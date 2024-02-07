import os
import yaml
from wrapper import *
from datetime import datetime
import utils.iptables as iptables
from utils.passgen import genPassword
from getpass import getpass
from glob import glob
boxes = {}
config_path = 'config.yml'
passwordFunc = lambda x: 'default'
seed="TotallySecureSeed1"
rounds=1000
with open(config_path, 'r') as file:
        data = yaml.safe_load(file)
def mkdir(path):
  try: return os.mkdir(path)
  except FileExistsError: return None

def Root_Password_Changes(box):
    mkdir(f"boxdata/{box}")
    if(os.path.isfile('boxdata/{box}/changedpassword')):
        root_password = genPassword(seed + box + "root",rounds)
    else:
        root_password=data["global"]["default_password"]
    default_password = passwordFunc(seed+box+"root")
    command = f'root:{root_password}\n'
    if(run_ssh_command(box,default_password,"chpasswd",stdinText=command) != -1):
        open(f"boxdata/{box}/changedpassword", "w").close()
    


def User_Password_Changes(box):
    if(os.path.isfile('boxdata/{box}/changedpassword')):
        default_password  = genPassword(seed + box + "root",rounds)
    else:
        default_password =data["global"]["default_password"]
    users = [i.split(":")[0] for i in run_ssh_command(box,default_password,"cat /etc/passwd", False).split("\n")]
    users.remove("root")
    users.remove("")
    mkpasswd = '\n'.join(f"{i}:{genPassword(seed+box[0] + i,rounds)}" for i in users)
    run_ssh_command(box,default_password ,"chpasswd",stdinText=mkpasswd)


def files_to_backup(box):
    if(os.path.isfile('boxdata/{box}/changedpassword')):
        default_password  = genPassword(seed + box + "root",rounds)
    else:
        default_password =data["global"]["default_password"]
    files_to_backup_entry = data.get('files_to_backup', [])
    for file in files_to_backup_entry:
        command = f'cp {file} /root/{file}'
        run_ssh_command(box,default_password,command)


def firewall_stuff(box):
     if(os.path.isfile('boxdata/{box}/changedpassword')):
        default_password  = genPassword(seed + box + "root",rounds)
     else:
        default_password =data["global"]["default_password"]
     mkdir(f"boxdata/{box}")
     command = "ss -naH4"
     stdout = run_ssh_command(box,default_password,command,False)
     iptables.UNRESTRICTED_SUBNETS = [data['global']['unrestricted_subnet']]
     bashscript = iptables.genFirewall(stdout)
     with open(f'boxdata/{box}/firewall.sh', 'w') as file:
            file.write(bashscript)
     print(bashscript)


def audit_Users(box):
    if(os.path.isfile('boxdata/{box}/changedpassword')):
        default_password  = genPassword(seed + box + "root",rounds)
    else:
        default_password =data["global"]["default_password"]
    users = [i.split(":")[0] for i in run_ssh_command( box,default_password,"cat /etc/passwd", False).split("\n")]
    mkdir(f"boxdata/{box}")
    with open(f'boxdata/{box}/users.txt', 'w') as file:
        for user in users:
            file.write(user+"\n")



def change_SSH_Settings(box):
    insert = [
        "PermitRootLogin yes",
        "PubkeyAuthentication no",
        "UseDNS no",
        "PermitEmptyPasswords no",
        "AddressFamily inet"
    ]
    if(os.path.isfile('boxdata/{box}/changedpassword')):
        default_password  = genPassword(seed + box + "root",rounds)
    else:
        default_password =data["global"]["default_password"]
    sshd_config = '\n'.join(insert) + '\n' + run_ssh_command(box,default_password,"cat /etc/ssh/sshd_config",False)
    run_ssh_command(box,default_password,"cat > /etc/ssh/sshd_config",stdinText=sshd_config)


def modify_php_settings(box):
    default_password = passwordFunc(seed+box+"root")
    php_settings = '\n'.join(f'{setting} = {value}' for setting, value in data.get('php_settings',{}).items()) + '\n'
    for php_ini in glob("/**/php.ini", recursive=True):
        php_ini_content  = run_ssh_command(box,default_password,f"cat '{php_ini}'")
        php_ini_content += php_settings
        run_ssh_command(box, default_password, f"cat > '{php_ini}'", stdinText= php_ini_content)

def change_sysctl_settings(box):
    default_password = passwordFunc(seed+box+"root")
    sysctl_conf  = '\n'.join(f'{setting} = {value}' for setting, value in data.get('sysctl_settings',{}).items()) + '\n'
    sysctl_conf += run_ssh_command(box,default_password,"cat /etc/sysctl.conf",False)
    run_ssh_command(box,default_password,"cat > /etc/sysctl.conf", stdinText=sysctl_conf)



def run_single_command(box,cmd):
    if(os.path.isfile('boxdata/{box}/changedpassword')):
        default_password  = genPassword(seed + box + "root",rounds)
    else:
        default_password =data["global"]["default_password"]
    run_ssh_command(box,default_password,cmd)

def execute_BashScript(script, box):
    default_password = boxes[box][0]
    try:
        with open(script, 'r') as bash_script:
            script_content = bash_script.read()

            run_ssh_command(box,default_password,script)



    except Exception as e:
        print(f"Error: {e}")
def enumerate(box):
    #WIP
    print("enum")

def fix_pam(box):
    #WIP
    print("pam")



functions = [audit_Users,Root_Password_Changes,User_Password_Changes,files_to_backup,firewall_stuff,execute_BashScript,change_SSH_Settings,modify_php_settings,change_sysctl_settings,run_single_command]
def exec_function(function_number):
     for line in open("boxes.conf"):
        if "#" not in line:
            ip_address = line.strip()
            root_password = passwordFunc(ip_address + "root")
            boxes[ip_address]=(root_password)
            functions[function_number](ip_address)



def main():
    global passwordFunc
    seed = getpass("seed: ")
    if input("Use seed? ") == 'y':
            passwordFunc = lambda x: genPassword(x,rounds)
    else:
            
            passwordFunc = lambda x: data['global']['default_password']
    while(True):
        print("\nSelect an option:")
        print("1. Audit Users")
        print("2. Root Password Changes")
        print("3. User Password Changes")
        print("4. Files Backup")
        print("5. Firewall Stuff")
        print("6. Execute Bash Script")
        print("7. Change SSH Settings")
        print("8. Modify PHP Settings")
        print("9. Change Sysctl Settings")
        print("10. Run Single Command")
        print("0. Exit")
        option = input("Enter the option number: ")
        if(int(option) > 0 and int(option) <= 10):
            exec_function(int(option)-1)
        elif(int(option)==0):
            break
main()