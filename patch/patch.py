import os
import shutil
import re

r=open("patch.txt","rb").read()


dst_dir=b"/home/stefan/projects/ioty_stefan/public/"
src_dir=b"/home/stefan/projects/ioty_own/"


def re_insert_after(content,ins,reg):
    match=re.search(reg,content,re.DOTALL)
    #print(content)
    print("===============")
    print(reg)
    print("================")
    p=match.span()[1] # end position
    print("content",match.span()[0],p)
    return content[:p]+ins+content[p:]

def insert_after(content,ins,search):
    p=content.find(search)
    p+=len(search)
    return content[:p]+ins+content[p:]

def re_insert_before(content,ins,reg):
    print("re_insert_before")
    #print(content)
    print("===============")
    print(reg)
    print("================")
    match=re.search(reg,content,re.DOTALL)
    p=match.span()[0] # start position
    print("content",p,match.span()[1])
    return content[:p]+ins+content[p:]

def insert_before(content,ins,search):
    p=content.find(search)
    return content[:p]+ins+content[p:]



patches=r.split(b'\n####\n')
pp=0
for patch in patches:
    rule=patch.split(b'\n###\n')
    cmd=rule[0].split(b'\n##\n')
    print(cmd,len(cmd))
    if len(cmd)==1:
        print(cmd[0])
        if cmd[0].strip()==b"copy_files":
            print("--> copy files")
            args=rule[1:]
            for arg in args:
                #print(arg)
                f1,f2=arg.split(b'\n##\n')
                f1=f1.strip()
                f2=f2.strip()
                sf=src_dir+f1
                df=dst_dir+f2
                print("copy ",sf,df,os.path.isfile(sf))
                # if os.path.isfile(sf):
                os.makedirs(os.path.dirname(df), exist_ok=True)
                shutil.copy(sf, df)
    elif len(cmd)==2:
        pp+=1
        filename=dst_dir+cmd[0].strip()
        command=cmd[1].strip()
        args=rule[1:]
        content=open(filename,'rb').read()
        print("red file",len(content))
        for arg in args:
            s1,s2=arg.split(b'\n##\n')
            print(filename,command)
            if command==b'insert_after':
                content=insert_after(content,s1,s2)
            elif command==b're_insert_after':
                 content=re_insert_after(content,s1,s2)
            elif command==b'insert_before':
                content=insert_before(content,s1,s2)
            elif command==b're_insert_before':
                 content=re_insert_before(content,s1,s2)
        #open(filename+b"_jnk",'wb').write(content)
        open(filename,'wb').write(content)
