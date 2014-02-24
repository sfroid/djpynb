import glob, os, shutil, time, traceback
import zipfile


# get list of files to backup
logfile = '../gotyourbackup.log'
dpath = "/home/sfroid/Dropbox/backups/sfroid"


def logMsg(msg):
    ef = open(logfile, 'a')
    ef.write("\n\n%s\n"%(str(time.ctime())))
    ef.write(msg)
    ef.write("\n")
    ef.close()


def fullPath(fp):
    return os.path.abspath(fp)

def getFilePaths(pat):
    return [fullPath(fp) for fp in glob.glob(pat)]

def getFilePathsToBackup():
    data = open('filesToBackup.txt').readlines()
    data = [ln.strip() for ln in data]
    data = [ln for ln in data if not (ln.startswith('#') or (ln == ''))]

    fs = []
    [fs.extend(getFilePaths(pat)) for pat in data]

    return fs


def copyFile(p1, p2):
    replace = False
    pdir = os.path.dirname(p2)
    if not os.path.exists(os.path.dirname(p2)):
        # create missing directories
        os.makedirs(pdir)
        replace = True
    else:
        if os.path.exists(p2):
            if os.path.getmtime(p1) > os.path.getmtime(p2):
                replace = True
        else:
            replace = True

    if replace is True:
        shutil.copy(p1, p2)
        return 1
    return 0

# copy files to dropbox folder
def moveZipToDropboxFolder(zfs):
    dest_file = os.path.join(dpath, os.path.basename(zfs))
    if os.path.exists(dest_file):
        os.remove(dest_file)
    return shutil.move(zfs, dpath)

def copyToBackupFolder(fs):
    dest_path = os.path.abspath("../backup")
    count = 0
    for f in fs:
        npath = os.path.join(dest_path, f[1:])
        count += copyFile(f, npath)
    return count

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))


def zipFilesInBackup():
    pfix = time.strftime('%A')
    zname = 'Backup_%s.zip'%pfix
    zipf = zipfile.ZipFile(zname, mode='w', compression=zipfile.ZIP_DEFLATED)

    cdir = os.getcwd()
    os.chdir("..")
    zipdir('backup', zipf)
    os.chdir(cdir)

    zipf.close()
    return zname

def makeMonthlyBackup(zname):
    nname = "Backup_%s.zip"%time.strftime("%d%b%Y")
    shutil.copy(zname, os.path.join(dpath, nname))

def cleanBackupFolder():
    removeBackupFolder()
    os.mkdir("../backup")

def removeBackupFolder():
    try:
        shutil.rmtree("../backup")
    except:
        pass

def runDbBackup():
    os.system("bash /home/sfroid/website/django/sfroid/runbackup.sh")


def doBackup():
    cleanBackupFolder()
    fs = getFilePathsToBackup()
    count = copyToBackupFolder(fs)
    zname = zipFilesInBackup()

    day = int(time.strftime("%d"))
    if day == 1:
        makeMonthlyBackup(zname)

    moveZipToDropboxFolder(zname)
    removeBackupFolder()
    
    # dbbackup
    runDbBackup()
    
    return count


def main():
    while 1:
        print "Getting your back right now!!",
        try:
            count = doBackup()
            print "Copied %d files."%count
            logMsg("Successfully performed backup. Copied %d files"%count)
        except:
            logMsg("%s\n%s"%("Ran into error", traceback.format_exc()))

        #time.sleep(10)
        time.sleep(12*60*60)

if __name__ == "__main__":
    #from pprint import pprint as pp
    #pp(getFilePathsToBackup())
    main()
