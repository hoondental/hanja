import os
import time
import datetime
import numpy as np
import random
from itertools import permutations
from IPython.display import clear_output

def read_hanjas(path):
    '''
    파일 경로를 입력받아 [(한자, 뜻, 음)] 리스트 반환함.
    '''
    with open(path, encoding='utf8') as f:
        lines = f.readlines()
    hanjas = []
    for line in lines:
        print(line)
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


def question0(hanja, num=None):
    '''
    한자, 뜻 음 을 보여줌
    '''
    prefix = '##########  ' + str(num) + '번  ########## \n' if num is not None else '############################\n'
    char, meaning, sound = hanja
    ans = input(prefix + f'{char}    {meaning}    {sound}\n\n' + '잘 알고 있는 한자이면 아무 글자나 입력후 엔터키를, 다시 공부하고 싶은 한자이면 그냥 엔터키를 입력하세요')
    if len(ans) > 0:
        return True
    else:
        return False



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
    


def hanja_practice(qtype, hanjas, thanjas, basic_iter=2, num_extra=100, num_examples=4):
    assert qtype in (0, 1, 2, 3)
    def question(hanja, num):
        if qtype == 0:
            return question0(hanja, num)
        elif qtype == 1:
            return question1(hanja, num)
        elif qtype == 2:
            return question2(hanja, hanjas, num_examples=num_examples, num=num)
        elif qtype == 3:
            return question3(hanja, num)
    
    wrong_score = {h: 2 + basic_iter for h in thanjas}
    
    print('^^^^^^^^^^ 전체 문제를 %d 회 반복합니다. ^^^^^^^^^^^' % basic_iter)
    time.sleep(2)
    clear_output(wait=True)
    for it in range(basic_iter): 
        _thanjas = [thanjas[i] for i in np.random.permutation(list(range(len(thanjas))))]
        for i, hanja in enumerate(_thanjas):
            clear_output(wait=True)
            correct = question(hanja, num=i+1)
            if correct:
                wrong_score[hanja] = max(1, wrong_score[hanja] / 2.0)
            else:
                wrong_score[hanja] *= 2.0
            clear_output(wait=True)
    
    print('^^^^^^^^^^ 문제 풀이 성적을 고려하여 %d 문제를 더 풀겠습니다. ^^^^^^^^^^^' % num_extra)
    time.sleep(2)      
    pcount = 0
    clear_output(wait=True)
    while pcount < num_extra:
        wrong_sum = sum(list(wrong_score.values()))
        wprob = [s / wrong_sum for s in wrong_score.values()]
        idxes = np.random.choice(list(range(len(thanjas))), 5, replace=False, p=wprob)
        for idx in idxes:
            pcount += 1
            hanja = thanjas[idx]
            clear_output(wait=True)
            correct = question(hanja, pcount)
            if correct:
                wrong_score[hanja] = max(1, wrong_score[hanja] / 2.0)
            else:
                wrong_score[hanja] *= 2.0
            print(wrong_score)
            time.sleep(1)
            clear_output(wait=True)
            if pcount == num_extra:
                break    
    
