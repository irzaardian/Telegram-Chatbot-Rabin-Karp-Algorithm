import mysql.connector
from nltk import ngrams
from operator import itemgetter
from datetime import datetime
from Processing import *

mydb = mysql.connector.connect(host='localhost',user='root',passwd='',database='chatsia')
sql = mydb.cursor()
P = Processing()

class Respons():
    def chatSIAResponse(self,input_text):
        sql.execute("select id, pertanyaan from pattern_template")
        hasil_sql = sql.fetchall()

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
        # stop_inputan = [P.stopword_removal(i) for i in space_inputan]
        print("================hasil stopword removal inputan================")
        print(stop_inputan)

        #stemming menggunakan sastrawi pada inputan
        stemming_inputan =P.stemming(stop_inputan)
        print("================hasil stemming inputan================")
        print(stemming_inputan)

        #Sinonim dan singkatan kata
        sinonim_inputan = P.sinonim(stemming_inputan)
        print("================hasil sinonim dan singkatan inputan================")
        print(sinonim_inputan)

        #menggabungkan kata pada inputan
        # final_text_inputan = ''.join(stemming_inputan)
        final_text_inputan = sinonim_inputan.replace(" ", "")
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

        print("type data pattern_template[x][1]")
        print(type(pattern_template))

        # stemming pattern template
        x=0
        while x < len(pattern_template):
            pattern_template[x][1] = P.stemming(pattern_template[x][1])
            x = x+1
        print("===========hasil stemming pattern template===========")
        print (pattern_template)

        #Sinonim dan singkatan kata
        x=0
        while x < len(pattern_template):
            pattern_template[x][1] = P.sinonim(pattern_template[x][1])
            x = x+1
        print("===========hasil sinonim pattern template===========")
        print (pattern_template)
   
        # merge list pattern template
        x=0
        while x < len(pattern_template):
            pattern_template[x][1] = pattern_template[x][1].replace(" ", "")
            x = x+1
        print("===========hasil merge pattern template===========")
        print (pattern_template)

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

        print("=============print(pattern_template[0][1])=============")
        print(hasil_inputan)
        print("=============print(pattern_template[0][1])=============")
        print(pattern_template[0][1])
        #irisan dan dice coeficient
        x = 0 
        while x < len(pattern_template):
            irisan = P.irisan(hasil_inputan, pattern_template[x][1])
            # irisan = list(set(hasil_inputan) & set(pattern_template[x][1]))
            temp = len(irisan)
            print("===============Irisan===============")
            print ("Irisan :",P.irisan(hasil_inputan, pattern_template[x][1]))
            # print ("Irisan :",list(set(hasil_inputan) & set(pattern_template[x][1])))
            print("Jumlah Irisan :",temp)
            print("Panjang Inputan :",len(hasil_inputan))
            print("Panjang Pattern :",len(pattern_template[x][1]))
            s = 2 * temp / (len(hasil_inputan) + len(pattern_template[x][1])) * 100
            pattern_template[x][1] = s
            x = x+1
        print("=============dice coeficient pattern template dan inputan user=============")
        print(pattern_template)

        #sorting pattern template
        pattern_template.sort(key=itemgetter(1), reverse=True)
        print("===============hasil sorting pattern template===============")
        print(pattern_template)

        nilai_similarity = pattern_template[0][1]
        id = pattern_template[0][0]

        data_log = []

        i = 0
        while i < 3 :
            temp = pattern_template[i]
            data_log.append(temp)
            i = i+1

        print("data log")
        print(data_log)

        if nilai_similarity <= 40:   
            validation = True
            return validation
        
        query = "select jawaban from pattern_template where id = '%s'" % (id)
        sql.execute(query)
        hasil_jawaban = sql.fetchone()

        print(hasil_jawaban)

        string_hasil_jawaban = ''
        for i in hasil_jawaban:
            string_hasil_jawaban = string_hasil_jawaban + i
        print(string_hasil_jawaban)

        return string_hasil_jawaban, data_log

    def simpan_penilaian (self,pertanyaan, log, kesimpulan):
        # query = "select jawaban from pattern_template where id = '%s'" % (id)
        # sql.execute(query)
        
        jawaban_log = []
        i = 0
        while i < len(log):
            query = "select pertanyaan, jawaban from pattern_template where id = '%s'" % (log[i][0])
            sql.execute(query)
            hasil_jawaban = sql.fetchone()
            jawaban_log.append(hasil_jawaban)
            i = i+1
    
        waktu = datetime.now()
        print(waktu)

        query = "INSERT INTO penilaian (log_date,pertanyaan,pattern,jawaban,persentase,kesimpulan) VALUES (%s,%s,%s,%s,%s,%s)"
        records_to_insert = [(waktu, pertanyaan, jawaban_log[0][0], jawaban_log[0][1],P.truncate(log[0][1],4),kesimpulan),
                            (waktu, pertanyaan, jawaban_log[1][0], jawaban_log[1][1],P.truncate(log[1][1],4),'Tidak Sesuai'),
                            (waktu, pertanyaan, jawaban_log[2][0], jawaban_log[2][1],P.truncate(log[2][1],4),'Tidak Sesuai')]

        sql.executemany(query, records_to_insert)
        mydb.commit()
