import os
import shutil

r=open("patch.txt").read()


dst_dir="/home/stefan/projects/github_ioty/ioty_pup/"
src_dir="/home/stefan/projects/github_ioty/ioty_own/"

def insert_after(content,ins,search):
    p=content.find(search)
    p+=len(search)
    return content[:p]+ins+content[p:]

def insert_before(content,ins,search):
    p=content.find(search)
    return content[:p]+ins+content[p:]



patches=r.split('####')
for patch in patches:
    rule=patch.split('###\n')
    cmd=rule[0].split('##\n')
    print(cmd)
    if len(cmd)==1:
        if cmd[0].strip()=="copy_files":
            args=rule[1:]
            for arg in args:
                f1,f2=arg.split('##\n')
                f1=f1.strip()
                f2=f2.strip()
                sf=src_dir+f1
                df=dst_dir+f2
                print("copy ",sf,df,os.path.isfile(sf))
                # if os.path.isfile(sf):
                os.makedirs(os.path.dirname(df), exist_ok=True)
                shutil.copy(sf, df)
    elif len(cmd)==2:
        filename=dst_dir+cmd[0].strip()
        command=cmd[1].strip()
        args=rule[1:]
        content=open(filename).read()
        print("red file",len(content))
        for arg in args:
           s1,s2=arg.split('##\n')
           print(filename,command,s1[:30],">>>>>>>>>>",s2[:30])

