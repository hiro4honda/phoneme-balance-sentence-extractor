# -*- coding: utf-8 -*-
import argparse
import sys
import os
import re
import pyopenjtalk


phoneVowel = ['a', 'i', 'u', 'e', 'o']
phoneConsonant = ['k', 'ky', 'kw', 'g', 'gy', 'gw', 's', 'sh', 'j', 'cl', 'ts', 'z', 't', 'ch', 'ty', 'd', 'dy', \
                  'n', 'ny', 'h', 'hy', 'b', 'by', 'p', 'py', 'f', 'm', 'my', 'y', 'ry', 'r', 'w', 'N', 'v']
phoneSpecial = ['pau', 'sil', 'xx']

# unvoiced fricative / unvoiced plosive
silentFricativePlosiveConsonant = ['s', 'sh', 'h', 'hy', 'f', 'k', 'ky', 'kw', 't', 'ts', 'ch', 'ty', 'p', 'py']

# nasal consonant
nasalConsonant = ['g', 'gy', 'gw', 'n', 'ny', 'm', 'my', 'N']

# half vowel
halfVowel = ['w','y']


def unknown_check(w):

    for i in range(0, len(phoneVowel)):
        if w == phoneVowel[i]:
            return

    for i in range(0, len(phoneConsonant)):
        if w == phoneConsonant[i]:
            return

    for i in range(0, len(phoneSpecial)):
        if w == phoneSpecial[i]:
            return

    print("phoneUnknown: %s" % w) 


def convert_phonemes(s):
    if len(s) > 1000:
        return ''
    ph = pyopenjtalk.g2p(s)
    w = ph.split()
    for i in range(0, len(w)):
        if w[i] == 'A':
            w[i] = 'a'
        elif w[i] == 'I':
            w[i] = 'i'
        elif w[i] == 'U':
            w[i] = 'u'
        elif w[i] == 'E':
            w[i] = 'e'
        elif w[i] == 'O':
            w[i] = 'o'
        
        unknown_check(w[i])

    t = ""
    for i in range(0, len(w)):
        t += w[i] + ' '
        
    return t[:-1]

def kata2hira(in_str):
    return "".join([chr(ord(ch) - 96) if ("ァ" <= ch <= "ヴ") else ch for ch in in_str])

def juman_postprocess(sentences):
    kana_sentences = []

    sentence = ''
    unknown_reading_word = False
    numeral_word = False

    for i in range(0, len(sentences)):
        w = sentences[i].split()
        
        if w[0] == '@':
            continue

        if w[0] == 'EOS':
            kana_sentences.append(sentence)
            sentence = ''

            unknown_reading_word = False
            numeral_word = False


        else:
            if -1 != sentences[i].find('読み不明'):
                unknown_reading_word = True

            if w[5] == '数詞':
                numeral_word = True

            sentence += kata2hira(w[1])


    return kana_sentences

def count_moura(sentences):
    moras = []

    for i in range(0, len(sentences)):
        
        mora = 0

        for j in range(0, len(sentences[i])):
            
            if sentences[i][j] != 'ゃ' and sentences[i][j] != 'ゅ' and sentences[i][j] != 'ょ'  and \
                sentences[i][j] != '「'  and sentences[i][j] != '」' and sentences[i][j] != '（' and sentences[i][j] != '）' and \
                sentences[i][j] != '、'  and sentences[i][j] != '。' and sentences[i][j] != '！' and sentences[i][j] != '？':
                mora += 1

        moras.append(mora)
        
    return moras

def remove_long_and_short_mora(in_org_sentences, in_kana_sentences, in_phonemes, in_moras):

    out_org_sentences = []
    out_kana_sentences = []
    out_phonemes = []
    out_mouras = []
    
    for i in range(0, len(in_moras)):
        if 10 > in_moras[i] or in_moras[i] > 67:
            continue

        out_org_sentences.append(in_org_sentences[i])
        out_phonemes.append(in_phonemes[i])
        out_kana_sentences.append(in_kana_sentences[i])
        out_mouras.append(in_moras[i])

    return out_org_sentences, out_kana_sentences, out_phonemes, out_mouras


# count two phoneme chain
def count_phoneme_chain2(phonemes):

    cv_dic = {}
    vc_dic = {}
    vv_dic = {}

    for i in range(0, len(phoneConsonant)):
        for j in range(0, len(phoneVowel)):
            cv_dic[phoneConsonant[i] + ' ' + phoneVowel[j]] = 0

    for i in range(0, len(phoneVowel)):
        for j in range(0, len(phoneConsonant)):
            vc_dic[phoneVowel[i] + ' ' + phoneConsonant[j]] = 0

    for i in range(0, len(phoneVowel)):
        for j in range(0, len(phoneVowel)):
            vv_dic[phoneVowel[i] + ' ' + phoneVowel[j]] = 0


    for i in range(0, len(phonemes)):
        w = phonemes[i].split()
        for j in range(1, len(w)):
            key = w[j-1] + ' ' + w[j]
            if key in cv_dic:
                val = cv_dic[key]
                cv_dic[key] = val + 1

            if key in vc_dic:
                val = vc_dic[key]
                vc_dic[key] = val + 1

            if key in vv_dic:
                val = vv_dic[key]
                vv_dic[key] = val + 1

    return cv_dic, vc_dic, vv_dic

# count three phoneme chain
def count_phoneme_chain3(phonemes):

    cvc1_dic = {}
    cvc2_dic = {}
    vcv_dic = {}

    for i in range(0, len(silentFricativePlosiveConsonant)):
        for j in range(0, len(phoneVowel)):
                for k in range(0, len(silentFricativePlosiveConsonant)):
                    cvc1_dic[silentFricativePlosiveConsonant[i] + ' ' + phoneVowel[j] + ' ' + silentFricativePlosiveConsonant[k]] = 0

    for i in range(0, len(nasalConsonant)):
        for j in range(0, len(phoneVowel)):
                for k in range(0, len(nasalConsonant)):
                    cvc2_dic[nasalConsonant[i] + ' ' + phoneVowel[j] + ' ' + nasalConsonant[k]] = 0

    for i in range(0, len(phoneVowel)):
        for j in range(0, len(halfVowel)):
                for k in range(0, len(phoneVowel)):
                    vcv_dic[phoneVowel[i] + ' ' + halfVowel[j] + ' ' + phoneVowel[k]] = 0


    for i in range(0, len(phonemes)):
        w = phonemes[i].split()
        for j in range(2, len(w)):
            key = w[j-2] + ' ' + w[j-1] + ' ' + w[j]
            if key in cvc1_dic:
                val = cvc1_dic[key]
                cvc1_dic[key] = val + 1

            if key in cvc2_dic:
                val = cvc2_dic[key]
                cvc2_dic[key] = val + 1

            if key in vcv_dic:
                val = vcv_dic[key]
                vcv_dic[key] = val + 1

    return cvc1_dic, cvc2_dic, vcv_dic

def extract_sentence(in_org_sentences, in_kana_sentences, in_phonemes, phoneme_chain):
    out_org_sentences = []
    out_phonemes = []
    out_kana_sentences = []

    phoneme_chain_nonzero = {}
    for k, v in phoneme_chain.items():
        if v != 0:
            phoneme_chain_nonzero[k] = v

    phoneme_chain_check = {}
    for k, v in phoneme_chain_nonzero.items():
        phoneme_chain_check[k] = 0

    phoneme_chain_sorted = sorted(phoneme_chain_nonzero.items(), key=lambda x:x[1])

    for i in range(0, len(phoneme_chain_sorted)):
        if phoneme_chain_check[phoneme_chain_sorted[i][0]] == 0:
            w1 = phoneme_chain_sorted[i][0].split()

            for j in range(0, len(in_phonemes)):
                find_chain = False
                w2 = in_phonemes[j].split()
                if len(w1) == 2:
                    for k in range(1, len(w2)):
                        if w1[0] == w2[k-1] and w1[1] == w2[k]:
                            find_chain = True
                            break

                elif len(w1) == 3:
                    for k in range(2, len(w2)):
                        if w1[0] == w2[k-2] and w1[1] == w2[k-1] and w1[2] == w2[k]:
                            find_chain = True
                            break

                if find_chain:
                    for k in range(1, len(w2)):
                        x = w2[k-1] + ' ' + w2[k]
                        if phoneme_chain_check.get(x) != None:
                            phoneme_chain_check[x] = 1

                    for k in range(2, len(w2)):
                        x = w2[k-2] + ' ' + w2[k-1] + ' ' + w2[k]
                        if phoneme_chain_check.get(x) != None:
                            phoneme_chain_check[x] = 1

                    out_org_sentences.append(in_org_sentences[j])
                    out_phonemes.append(in_phonemes[j])
                    out_kana_sentences.append(in_kana_sentences[j])

                    break


    return out_org_sentences, out_kana_sentences, out_phonemes

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='balance sentence extractor')
    parser.add_argument('--in-org-file',help='original sentences')
    parser.add_argument('--in-juman-file',help='parsed sentences by juman')
    parser.add_argument('--out-file',help='extracted sentences')
    args = parser.parse_args()

    fp = open(args.in_org_file, 'r')
    org_sentences = fp.readlines()
    fp.close()

    fp = open(args.in_juman_file, 'r')
    juman_sentences = fp.readlines()
    fp.close()

    kana_sentences = juman_postprocess(juman_sentences)
    moras = count_moura(kana_sentences)

    phonemes = []
    for i in range(0, len(kana_sentences)):
        phonemes.append(convert_phonemes(kana_sentences[i]))

    org_sentences, kana_sentences, phonemes, moras = \
                remove_long_and_short_mora(org_sentences, kana_sentences, phonemes, moras)

    phoneme_chain ={}
    cv_dic, vc_dic, vv_dic = count_phoneme_chain2(phonemes)
    phoneme_chain.update(cv_dic)
    phoneme_chain.update(vc_dic)
    phoneme_chain.update(vv_dic)

    cvc1_dic, cvc2_dic, vcv_dic = count_phoneme_chain3(phonemes)
    phoneme_chain.update(cvc1_dic)
    phoneme_chain.update(cvc2_dic)
    phoneme_chain.update(vcv_dic)

    extracted_org_sentences, extracted_kana_sentences, extracted_phonemes = \
                 extract_sentence(org_sentences, kana_sentences, phonemes, phoneme_chain)

    fp = open(args.out_file, 'w')
    for i in range(0, len(extracted_org_sentences)):
        fp.write(extracted_org_sentences[i])
    fp.close()

