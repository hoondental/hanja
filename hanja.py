import os
import time
import datetime
import numpy as np


def read_hanjas(path):
    '''
    파일 경로를 입력받아 [(한자, 뜻, 음)] 리스트 반환함.
    '''
    with open(path, encoding='utf8') as f:
        lines = f.readlines()
    hanjas = []
    for line in lines:
        char, meaning, sound = line.strip().split()
        hanjas.append((char, meaning, sound))
    return hanjas



def read_level_hanjas(dir_db, levels):
    '''
    한자 파일의 폴더와, [레벨] 리스트를 입력받아 {레벨:[(한자,뜻,음)]} 형태의 딕셔너리를 반환함.
    '''
    level_hanjas = {}
    hanjas = []
    for level in levels:
        fname = level + '.txt'
        path = os.path.join(dir_db, fname)
        if not os.path.isfile(path):
            print(level, '의 한자 파일 경로가 잘못되었습니다.', path)
            continue
        _hanjas = read_hanjas(path)
        level_hanjas[level] = _hanjas
        hanjas.extend(_hanjas)
    return hanjas, level_hanjas


def question1(hanja, num=None):
    '''
    한자를 보여주고 뜻과 음을 입력
    '''
    prefix = '##########  ' + str(num) + '번  ########## \n' if num is not None else '############################\n'
    char, meaning, sound = hanja
    answered = False
    for i in range(3):
        try:
            ans = input(prefix + char + ' 의 뜻과 소리를 쓰시오     ')
            m, s = ans.strip().split()
        except:
            print('한자의 뜻과 소리를 띄어서 입력하세요')
            continue
        else:
            answered = True
            break
    if answered and m == meaning and s == sound:
        correct = True
        print('맞았습니다. 축하합니다')
    else:
        correct = False
        print('틀렸습니다. 이 한자는 %s %s 입니다.' % (meaning, sound))
    time.sleep(1)
    return correct
                

def question2(hanja, hanjas, num_examples=5, num=None):
    '''
    한자의 뜻과 음을 알려주고 한자를 고르는 문제
    hanjas = [(한자,뜻,음)] 의 리스트, 보기가 출제될 한자들
    '''
    prefix = '##########  ' + str(num) + '번  ########## \n' if num is not None else '############################\n'
    char, meaning, sound = hanja
    chars = [h[0] for h in hanjas]
    examples = np.random.choice(chars, num_examples, replace=False)
    indexes = list(range(num_examples))
    if char in examples:
        idx = examples.tolist().index(char)
    else:
        idx = np.random.choice(indexes)
        examples[idx] = char
    answered = False
    for i in range(3):
        try:
            _examples = '   '.join(['(' + str(i+1) +')' + c  for i, c in enumerate(examples)])
            ans = input(prefix + '다음 보기들중 %s %s 자를 고르세요' % (meaning, sound) + '\n' + _examples + '     ')           
            _idx = int(ans) - 1
            assert _idx in indexes
        except:
            print('보기에서 맞는 한자를 골라 번호(숫자)를 입력하세요')
            continue
        else:
            answered = True
            break
    if answered and _idx == idx:
        correct = True
        print('맞았습니다. 축하합니다')
    else:
        correct = False
        print('틀렸습니다. %s %s 자는 %d번입니다' % (meaning, sound, idx+1))
    time.sleep(1)
    return correct

def question3(hanja, num=None):
    '''
    한자의 뜻과 음을 알려주고 스스로 써보도록 하는 문제
    몇초 후 답을 보여줌
    '''    
    prefix = '##########  ' + str(num) + '번  ########## \n' if num is not None else '############################\n'
    char, meaning, sound = hanja
    input(prefix + '%s %s 자를 노트에 써보세요, 다 쓴 후에 아무글자나 입력하세요     ' % (meaning, sound))
    print(char, ' 답이 맞았는지 확인하고 틀렸으면 답을 보고 다시 써보세요')
    ans = input('맞았으면 1, 틀렸으면 2를 입력해주세요     ')
    try:
        ans = int(ans)
    except:
        return False
    else:
        if ans == 1:
            return True
        else:
            return False
    

