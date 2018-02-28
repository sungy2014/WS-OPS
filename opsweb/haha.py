def check_pwd(str):
    r = 0
    for cc in str:
        if 'A' <= cc <= 'Z' or 'a' <= cc <= 'z':
            r = r | 1
        if '0' <= cc <= '9':
            r = r | 2
        if cc in "~!@#$%^&*().":
            r = r | 4
    print ('r', r)
    return r

if __name__ == "__main__":
    check_pwd('China_2018!')
