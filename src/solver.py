import subprocess, time, tempfile
import src.settings as settings
import tempfile
import os
import datetime
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

custom_temp_dir = r"/home/cass/Webstorm_project/0226/results/Regression_cases"  # 临时目录
if not os.path.exists(custom_temp_dir):
    os.makedirs(custom_temp_dir)


def run_command(command):
    start = time.time()
    # print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf-8')
    proc_stdout, proc_stderr = process.communicate()
    wall_time = time.time() - start

    # proc_stdout = proc_stdout
    # proc_stderr = proc_stderr
    # print(command)
    out_lines = str(proc_stdout)
    err_lines = str(proc_stderr)
    if wall_time > settings.timeout:
        err_lines += str(" timeout expired ")
    return out_lines, err_lines, wall_time

def run_solver(instance, solver, type):
    tfile = tempfile.NamedTemporaryFile(delete=False, dir=custom_temp_dir, suffix=".smt2")
    if type == 'z3str3':
        op = 'smt.string_solver=' + 'z3str3'
    elif type == 'z3seq':
        op = 'smt.string_solver=' + 'seq'
    elif type == 'fp':
        op = ''
    elif type == 'cvc5':
        op = '--strings-exp'

    else:
        op = ''
    case_former = str(instance)
    if "4.8.9" not in solver:
        case_former = case_former.replace('str.from_int', 'str.from.int')
        case_former = case_former.replace('str.in_re', 'str.in.re')
        case_former = case_former.replace('str.to_int', 'str.to.int')
        case_former = case_former.replace('str.to_re', 'str.to.re')
        case_former = case_former.replace('str.from_int', 'str.from.int')

        case_former = case_former.replace('str.from-int', 'str.from.int')
        case_former = case_former.replace('str.in-re', 'str.in.re')
        case_former = case_former.replace('str.to-int', 'str.to.int')
        case_former = case_former.replace('str.to-re', 'str.to.re')

    outFile = open(tfile.name, 'w')
    outFile.write(str(case_former))
    # outFile.write(f"{str(case_former)} - 时间: {current_time}")
    outFile.close()
    out, err, time = run_command(
        "timeout " + str(settings.timeout + 1) + " bash -c \'/home/cass/Webstorm_project/0226/" + solver + "/bin/z3 " + op + " " + outFile.name + "\'")

    # print('solver:', solver)
    # print('run time:', time)
    # print('out:', out)
    # print('err', err)
    # print(outFile.name)
    if time > settings.timeout:
        return 'timeout', time, out + err

    if out.lower().find('sat') != -1 or out.lower().find('unsat') != -1:
        return out.lower(), time, out + err
        
    return 'err', time, out + err
