#!/usr/bin/python

# Fetch GTFS feeds for SEPTA, NJ TRANSIT, PATCO, and Delaware First State.
# Based on https://gist.github.com/flibbertigibbet/8092373
import datetime
import csv
import os
import pickle
import subprocess
import zipfile

import requests
from bs4 import BeautifulSoup

class FeedFetcher():
  def __init__(self, ddir=os.getcwd(), get_nj=False, nj_username='', nj_pass=''):
    self.ddir = ddir
    self.get_nj = get_nj # whether to fetch from NJ TRANSIT or not
    self.tc = {} # time checks for GTFS fetches
    self.new_use = [] # list of new feeds successfully downloaded and validated
    self.nj_payload = {'userName': nj_username, 'password': nj_pass}
    if get_nj and (not nj_username or not nj_pass):
      self.get_nj = False
      print("Cannot fetch from NJ TRANSIT without nj_username and nj_pass specified.")

  def verify(self, file_name):
    # file_name is local to download directory
    f = os.path.join(self.ddir, file_name)
    if not os.path.isfile(f):
      print("File " + f + " not found; cannot verify it.")
      return False

    print("Validating feed in " + file_name + "...")
    try:
      p = subprocess.Popen(['feedvalidator.py', '--output=CONSOLE',
        '-m', '-n', f], stdout=subprocess.PIPE)
      out = p.communicate()
      res = out[0].split('\n')
      errct = res[-2:-1][0] # output line with count of errors/warnings
      if errct.find('error') > -1:
        print("Feed validator found errors in " + file_name + ":  " + errct + ".")
        return False
      elif out[0].find('this feed is in the future,') > -1:
        print("Feed validator found GTFS not in service until future for " +
          file_name + ".")
        return False
      else:
        if errct.find('successfully') > -1:
          print("Feed " + file_name + " looks great:  " + errct + ".")
        else:
          # have warnings
          print("Feed " + file_name + " looks ok:  " + errct[7:] + ".")
        return True
    except:
      print("Failed to run feed validator on GTFS " + file_name + ".")
      return False

    print("How did we get here?  In GTFS validation for " + file_name + ".")
    return False # shouldn't get here

  def check_header_newer(self, url, file_name):
    # return 1 if newer file available to download;
    # return 0 if info missing;
    # return -1 if current file is most recent.
    if self.tc.has_key(file_name):
      last_info = self.tc.get(file_name)
      hdr = requests.head(url)
      hdr = hdr.headers
      if hdr.get('last-modified'):
        last_mod = hdr.get('last-modified')
        if last_mod == last_info:
          print("No new download available for " + file_name + ".")
          return -1
        else:
          print("New download available for " + file_name + ".")
          print("Last downloaded: " + last_info + ".")
          print("New download posted: " + last_mod + ".")
          return 1
      else:
        print("No last-modified header set for " + file_name + " download link.")
        return 0
    else:
      print("Time check entry for " + file_name + " not found.")
      return 0

    # shouldn't happen
    print("How did we get here?  Failed checking header info.")
    return 0

  def get_stream(self, url, file_name, do_stream=True, session=None, do_verify=True):
    if self.check_header_newer(url, file_name) == -1:
      return False
    # file_name is local to download directory
    f = os.path.join(self.ddir, file_name)
    print("Getting file " + f + "...")
    if not session:
      stream = requests.get(url, stream=do_stream)
    else:
      stream = session.get(url, stream=do_stream)

    if stream.ok:
      stream_file = open(f, 'wb')
      if do_stream:
        for chunk in stream.iter_content():
          stream_file.write(chunk)
      else:
        stream_file.write(stream.content)

      stream_file.close()
      info = os.stat(f)
      if info.st_size < 10000:
        # file smaller than 10K may not be a GTFS; just warn
        print('Warning:')
        print("Download for " + f + " is only " + str(info.st_size) + " bytes.")
        print("It may not be a valid GTFS.")
      if not zipfile.is_zipfile(f):
        print("BAD DOWNLOAD FOR " + f + ".")
        print("Download for " + f + " is not a zip file.")
        return False
      if stream.headers.get('last-modified'):
        self.tc[file_name] = stream.headers.get('last-modified')
      else:
        # format like last-modified header
        self.tc[file_name] = datetime.datetime.utcnow(
          ).strftime("%a, %d %b %Y %H:%M:%S GMT")
      print("Download completed successfully.")
      # verify download
      if do_verify:
        if self.verify(file_name):
          print("GTFS verification succeeded.")
          self.new_use.append(file_name)
          return True
        else:
          print("GTFS verification failed.")
          return False
      else:
        print("Skipping GTFS verification in get_stream.")
        # not adding to new_use here; do elsewhere
        return True
    else:
      print("DOWNLOAD FAILED FOR " + f + ".")

    return False

  def fetch(self):
    # pickled log of last times downloaded
    time_check = os.path.join(self.ddir, 'time_checks.p')
    if os.path.isfile(time_check):
      tcf = open(time_check, 'rb')
      self.tc = pickle.load(tcf)
      tcf.close()
      print("Loaded time check file.")
      if self.tc.has_key('last_check'):
        last_check = self.tc['last_check']
        print("Last check: ")
        print(last_check)
        timedelt = datetime.datetime.now() - last_check
        print("Time since last check: " )
        print(timedelt)
    else:
      print("Will create new time check file.")

    self.tc['last_check'] = datetime.datetime.now()

    # call feed functions here
    self.get_nj_feeds()
    self.get_septa_feeds()
    self.get_delaware_feed()
    self.get_patco_feed()

    print("Downloading finished.  Writing time check file...")
    tcf = open(time_check, 'wb')
    pickle.dump(self.tc, tcf)
    tcf.close()
    print("Time check file written.")
    print("Writing 'new_use.csv', file of validated new downloads...")
    nu = open('new_use.csv', 'wb')
    nuw = csv.writer(nu)
    for n in self.new_use:
      print("Got new GTFS " + n)
      nuw.writerow([n])

    nu.close()
    print("Done writing 'new_use.csv'.")
    print("All done!")
    ###############################

  #################################
  # FEED FETCHING FUNCTIONS. FUN!
  ##################################

  ######### NJ TRANSIT SESSION ######################
  def get_nj_feeds(self):
    if self.get_nj:
      nj_login_url = 'https://www.njtransit.com/mt/mt_servlet.srv?hdnPageAction=MTDevLoginSubmitTo'
      s = requests.Session()
      s.post(nj_login_url, data=self.nj_payload)

      nj_rail_url = 'https://www.njtransit.com/mt/mt_servlet.srv?hdnPageAction=MTDevResourceDownloadTo&Category=rail'
      nj_bus_url = 'https://www.njtransit.com/mt/mt_servlet.srv?hdnPageAction=MTDevResourceDownloadTo&Category=bus'

      self.get_stream(nj_rail_url, 'nj_rail.zip', session=s)
      self.get_stream(nj_bus_url, 'nj_bus.zip', session=s)

      s.close()
    else:
      print("Skipping NJ data fetch.")
  ########## END NJ TRANSIT SESSION ##################

  ### SEPTA #####
  # get html page and check last updated date
  # (Last-Modified header not present)
  def get_septa_feeds(self):
    get_septa = True
    septa_file = 'septa.zip'
    page = requests.get('http://www2.septa.org/developer/')
    print("Checking last SEPTA update time...")
    last_mod = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")

    if page.ok:
      bs = BeautifulSoup(page.text)
      last_mod = bs.find('div', 'col_content').find('p').text
      print(last_mod)
      last_mod = last_mod[14:] # trim out date string
      if self.tc.has_key(septa_file):
        got_last = self.tc.get(septa_file)
        if got_last == last_mod:
          print("No new download available for SEPTA.")
          get_septa = False
        else:
          print("New SEPTA download available.")
          print("Latest update: " + last_mod + ".")
          print("Previous update: " + got_last + ".")
      else:
        print("No previous SEPTA download found.")
    else:
      print('failed to get SEPTA dowload info page.')

    if get_septa:
      if self.get_stream('http://www2.septa.org/developer/download.php',
      septa_file, do_verify=False):
        # extract bus and rail GTFS files from downloaded zip
        z = zipfile.ZipFile(septa_file)
        if len(z.namelist()) == 2:
          z.extractall(path=self.ddir)
          self.tc[septa_file] = last_mod
          z.close()
          # verify extracted GTFS zips
          if os.path.isfile('google_bus.zip') and os.path.isfile('google_rail.zip'):
            if self.verify('google_bus.zip'):
              self.new_use.append('google_bus.zip')
              if self.verify('google_rail.zip'):
                self.new_use.append('google_rail.zip')
                print("SEPTA GTFS files passed verification.")
              else:
                print("SEPTA rail GTFS verification failed.")
            else:
              print("SEPTA bus GTFS verification failed.")
          else:
            print("Could not find SEPTA GTFS files with expected names.")
        else:
          print("Unexpected contents in SEPTA zip file download:")
          print(z.namelist())
          print('Expected two files, but got %d.' % len(z.namelist()))
          print("Not extracting SEPTA zip.\n")
          z.close()

        # delete download file once the two GTFS zips in it are extracted
        os.remove(septa_file)
    ###############
    # END SEPTA
    ###############

  #### DELAWARE FIRST STATE ######
  def get_delaware_feed(self):
    de_url = 'http://dartfirststate.com/information/routes/gtfs_data/dartfirststate_de_us.zip'
    self.get_stream(de_url, 'dart.zip')
  ################################

  ###########################
  # check PATCO repo for updates
  def get_patco_feed(self):
    got_repo = False
    just_cloned = False
    patco_filename = 'patco.zip'
    start_dir = os.getcwd()

    try:
      os.chdir('patco-gtfs')
      got_repo = True
    except:
      print("Could not find patco-gtfs repository directory.  Checking out now...")

    if not got_repo:
      try:
        subprocess.check_call(['git', 'clone',
          'https://github.com/flibbertigibbet/patco-gtfs.git'])
        os.chdir('patco-gtfs')
        got_repo = just_cloned = True
      except:
        got_repo = just_cloned = False
        print("Failed to check out patco-gtfs repository.  Not getting PATCO GTFS.")

    try:
      behind = False
      if got_repo and not just_cloned:
        subprocess.check_call(['git', 'fetch'])

        # number of commits behind remote
        p = subprocess.Popen(['git', 'rev-list', 'HEAD..HEAD@{upstream}'],
          stdout=subprocess.PIPE)
        behind = p.communicate()[0]
        if behind:
          print("New changes found for patco-gtfs repo.  Merging...")
          subprocess.check_call(['git', 'pull'])
        else:
          print("No new changes found for patco-gtfs repository.")

      if just_cloned or behind:
        print("Building new PATCO GTFS...")
        subprocess.check_call(['python', 'make_calendar_dates.py'])
        subprocess.check_call(['python', 'make_fare_rules.py'])
        subprocess.check_call(['python', 'make_trips_stops.py'])
        os.chdir('gtfs_files')
        # zip it
        z = zipfile.ZipFile(open(os.path.join(start_dir, patco_filename),
          'wb'), mode='w')
        with z:
          for p, d, fs in os.walk(os.getcwd()):
            for f in fs:
              if f.endswith('.txt'):
                z.write(f)

          z.close()
          print("New PATCO GTFS written.  Validating...")
          if self.verify(patco_filename):
            print("New PATCO GTFS is valid.")
            # format like last-modified header
            self.tc[patco_filename] = datetime.datetime.utcnow(
              ).strftime("%a, %d %b %Y %H:%M:%S GMT")
            self.new_use.append(patco_filename)
          else:
            print("New PATCO GTFS is invalid.")
    except:
      print("Encountered an error while fetching/creating PATCO GTFS data.")

    os.chdir(start_dir) # back to where we were
    ###########################
    # END PATCO
    ###########################
