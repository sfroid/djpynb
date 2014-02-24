import os, time, glob
from pprint import pprint as pp

def ip2html_name(n1):
    if n1.endswith('.ipynb'):
        return n1[:-5] + 'html'
    raise

def getRootName(fn):
    return os.path.splitext(os.path.basename(fn))[0]

def get_file_dates(dr, ext):
    ip_files = {}
    for fname in glob.glob(dr + '/*.' + ext):
        tm = os.path.getmtime(fname)
        ip_files[getRootName(fname)] = tm
    return ip_files

def find_outdated_files(ifs, hfs):
    # find ipynb files which have not been updated recently
    outdated_files = []
    for fn, dt  in ifs.items():
        if fn not in hfs:
            outdated_files.append(fn)
        elif hfs[fn] < dt:
            outdated_files.append(fn)
    return outdated_files

def update_outdated_files(fls):
    for fl in fls:
        cmd1 = "ipython nbconvert --profile=nbserver_html --to html \"../notebooks/%s.ipynb\""%fl
        cmd2 = "mv \"%s.html\" ../html"%fl
        if os.system(cmd1):
            print "Error while running external command:\n%s"%cmd1
        elif os.system(cmd2):
            print "Error while running external command:\n%s"%cmd2
        else:
            print "Successfully updated html for %s"%fl


def check_custom_css():
    replace = False
    try:
        fp1 = '/home/sfroid/.config/ipython/profile_nbserver_html/static/custom/custom.css'
        fp2 = '/home/sfroid/website/pynb/html/custom.css'
        dt1 = os.path.getmtime(fp1)
        dt2 = os.path.getmtime(fp2)
        replace = (dt1 > dt2)
    except:
        replace = True

    if replace:
        os.system("cp %s %s"%(fp1, fp2))
        print "Copied custom.css"

def check_custom_html_css():
    """This method keeps track of the changes in the main notebook custom.css file
    and updates the html profile custom.css if anyting changes"""
    replace = False
    try:
        fp1 = '/home/sfroid/.config/ipython/profile_nbserver/static/custom/custom.css'
        fp2 = '/home/sfroid/.config/ipython/profile_nbserver_html/static/custom/custom.css'
        html_css = 'custom_html.css'
        dt1 = os.path.getmtime(fp1)
        dt2 = os.path.getmtime(fp2)
        replace = (dt1 > dt2)
    except:
        replace = True

    try:
        dt3 = os.path.getmtime(html_css)

        replace = replace or (dt3 > dt2)
    except:
        replace = True

    if replace:
        data = open(fp1).read() + '\n' + open(html_css).read()
        fd = open(fp2, 'w')
        fd.write(data)
        fd.close()
        print "Updated custom html css file"




def mainloop():
    while True:
        curr_dir = '../notebooks'
        dest_dir = '../html'
        ipynb_files = get_file_dates(curr_dir, 'ipynb')
        html_files = get_file_dates(dest_dir, 'html')

        odfiles = find_outdated_files(ipynb_files, html_files)

        update_outdated_files(odfiles)

        check_custom_html_css()
        check_custom_css()
        time.sleep(5)

if __name__ == '__main__':
    mainloop()
