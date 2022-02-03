import mysql.connector
import PreProcessing as P
from nltk import ngrams
from copy import copy, deepcopy


mydb = mysql.connector.connect(host='localhost',user='root',passwd='',database='chatbot')
sql = mydb.cursor()

sql.execute("select id, pertanyaan from pattern_template")
hasil_sql = sql.fetchall()
# print (hasil_sql)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def ChatbotResponse(input_text):
    #proses pre-processing pengguna======================================================================================================================================================
    #tokenisasi inputan
    token_inputan = P.tokenizing(input_text)
    print("================hasil tokenisasi inputan================")
    print (token_inputan)

    #mengubah inputan menjadi lowercase
    lowercase_inputan = P.case_folding(token_inputan)
    print("================hasil lower case inputan================")
    print (lowercase_inputan)

    #membuang tanda baca / punctuation removal pada inputan
    remove_inputan = [P.punctuation_removal_inputan(i) for i in lowercase_inputan]
    print("================hasil punctuation removal inputan================")
    print (remove_inputan)

    #membuang spasi pada inputan
    space_inputan = P.remove_space(remove_inputan)
    print("================hasil space removal inputan================")
    print (space_inputan)

    #membuang stopword/kata tidak penting pada inputan
    stop_inputan = P.stopword_removal(space_inputan)
    print("================hasil stopword removal inputan================")
    print(stop_inputan)

    #menggabungkan kata pada inputan
    final_text_inputan = ''.join(stop_inputan)
    print("================hasil merge inputan================")
    print(final_text_inputan)

    #mengubah kedalam bentuk bigram pada inputan
    bigram_inputan = list(ngrams(final_text_inputan, 2))
    print("================hasil bigram inputan================")
    print (bigram_inputan)

    #konversi ascii pada inputan
    konversi_inputan = P.konversi_ascii(bigram_inputan)
    print("================hasil konversi ascii inputan================")
    print (konversi_inputan)

    #Rolling hash inputan
    hasil_inputan = P.rolling_hash(konversi_inputan)
    print("================hasil rolling hash inputan================")
    print(hasil_inputan)

    #proses pre-processing pattern template==========================================================================================================================================
    print("================hasil sql================")
    print (hasil_sql)

    #konversi list of tupel to list
    pattern_template = [list(x) for x in hasil_sql]
    print("===========hasil konversi pattern template===========")
    print(pattern_template)

    #Tokenisasi pattern template
    x=0
    while x < len(pattern_template):
        pattern_template[x][1] = P.tokenizing(pattern_template[x][1])
        x = x+1
    print("===========hasil tokenisasi pattern template===========")
    print (pattern_template)

    #lowercase pattern template
    x=0
    while x < len(pattern_template):
        pattern_template[x][1] = P.case_folding(pattern_template[x][1])
        x = x+1
    print("===========hasil lower case pattern template===========")
    print (pattern_template)

    #punctuation pattern template
    x=0
    while x < len(pattern_template):
        pattern_template[x][1] = P.punctuation_removal(pattern_template[x][1])
        x = x+1
    print("===========hasil punctuation removal pattern template===========")
    print (pattern_template)

    #stopword pattern template
    x=0
    while x < len(pattern_template):
        pattern_template[x][1] = P.stopword_removal(pattern_template[x][1])
        x = x+1
    print("===========hasil stopword removal pattern template===========")
    print (pattern_template)

    olahan_pattern_template = deepcopy(pattern_template)

    #merge list pattern template
    x=0
    while x < len(pattern_template):
        pattern_template[x][1] = ''.join(pattern_template[x][1])
        x = x+1
    print("===========hasil merge pattern template===========")
    print (pattern_template)

    #merge list olahan pattern template
    x=0
    while x < len(olahan_pattern_template):
        olahan_pattern_template[x][1] = ' '.join(olahan_pattern_template[x][1])
        x = x+1
    print("===========hasil merge olahan pattern template===========")
    print (olahan_pattern_template)

    #konversi bigram pattern template
    x=0
    while x < len(pattern_template):
        pattern_template[x][1] = list(ngrams(pattern_template[x][1], 2))
        x = x+1
    print("===========hasil bigram pattern template===========")
    print (pattern_template)

    #konversi bigram ke ascii pattern template
    x=0
    while x < len(pattern_template):
        pattern_template[x][1] = P.konversi_ascii(pattern_template[x][1])
        x = x+1
    print("=============hasil konversi ascii pattern template=============")
    print (pattern_template)

    #Rolling hash pattern template
    x=0
    while x < len(pattern_template):
        pattern_template[x][1] = P.rolling_hash(pattern_template[x][1])
        x = x+1
    print("=============hasil rolling hash pattern template=============")
    print (pattern_template)

    print (len(pattern_template[1][1]))
    print (len(hasil_inputan))

    #irisan dan dice coeficient
    x = 0 
    while x < len(pattern_template):
        irisan = intersection(hasil_inputan, pattern_template[x][1])
        temp = len(irisan)
        print(temp)
        s = 2 * temp / (len(hasil_inputan) + len(pattern_template[x][1])) * 100
        pattern_template[x][1] = s
        x = x+1
    print("=============dice coeficient pattern template dan inputan user=============")
    print(pattern_template)

    #Sorting nilai persentase yang paling tinggi
    print("=============sorting persentase yang paling tinggi=============")
    pattern_template = sorted(pattern_template,key=lambda l:l[1], reverse=True)
    print (pattern_template)

    id = str(pattern_template[0][0]) #index [0][0] karena sebelumnya sudah di sorting
    print(id)
    print("id tertinggi = " + id)

    print("=============pattern template=============")
    print(pattern_template)
    print("=============olahan pattern template=============")
    print(olahan_pattern_template)

    if pattern_template[0][1] <= 50:   #index [0][1] karena sebelumnya sudah di sorting, index [0][1] merupakan hasil persentase, 50 merupakan nilai penentu minimal similarity
        # if pattern_template[0][1] > 30:
        #     balasan = "Apakah maksud anda "
        #     x = 0
        #     while x < len(pattern_template):
        #         if str(pattern_template[0][0]) == str(olahan_pattern_template[x][0]):
        #             hasil_jawaban = olahan_pattern_template[x][1]
        #         x = x+1
        #     print(hasil_jawaban)
        #     pesan = balasan + hasil_jawaban + " ?"
        #     return pesan
        pesan = "Pertanyaan tidak dapat dimengerti"
        return pesan
    
    query = "select jawaban from pattern_template where id = '%s'" % (id)
    sql.execute(query)
    hasil_jawaban = sql.fetchone()
    print("line 202")
    print(hasil_jawaban)

    string_hasil_jawaban = ''
    for i in hasil_jawaban:
        string_hasil_jawaban = string_hasil_jawaban + i
    print(string_hasil_jawaban)

    return string_hasil_jawaban

def simpan_penilaian (pertanyaan, jawaban, kesimpulan):
    # query = "select jawaban from pattern_template where id = '%s'" % (id)
    # sql.execute(query)
    query = "INSERT INTO penilaian (pertanyaan, jawaban, kesimpulan) VALUES (%s, %s,%s)"
    val = (pertanyaan, jawaban, kesimpulan)
    sql.execute(query, val)
    mydb.commit()
    # print(pertanyaan)
    # print(jawaban)
    # print(kesimpulan)
