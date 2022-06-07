import nltk
import math
import string
from flashtext import KeywordProcessor
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk import *

class Processing():
    def tokenizing (self,input):
        text = nltk.word_tokenize(input)
        return text

    def case_folding (self,input):
        text = [i.casefold() for i in input]
        return text

    def punctuation_removal_inputan(self,input):
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for i in input:
            if i in punc:
                input = input.replace(i, "")
        return input

    def punctuation_removal(self,input):
        input = list(filter(lambda token: token not in string.punctuation, input))
        return input

    def remove_space(self,input):
        x = 0
        while x < len(input):
            if input[x] == '':
                del input[x]
            x = x+1
        return input

    def stopword_removal(self,input):
        #Stopword sastrawi
        stop_factory = StopWordRemoverFactory().get_stop_words()
        more_stopword = [
            'bagaimana',
            'siapa',
            'apa',
            'bagaimanakah',
            'siapakah',
            'mengajukan',
            'penulisan',
            'program',
            'semester',
            'sekarang',
            'laporan',
            'contoh',
            'meminta',
            'berapa',
            'judul',
            'download',
            'lihat',
            'peserta',
            'yg',
            'perihal',
            'mau',
            'error',
            'isi',
            'lg',
            'tanya',
            'kapan'
            ]
        # Tambahkan Stopword Baru
        stop_words = stop_factory+more_stopword

        dictionary = ArrayDictionary(stop_words)
        str = StopWordRemover(dictionary)

        filtered_sentence = [w for w in input if not w.lower() in stop_words]
        return filtered_sentence

    def stemming(self,input):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        hasil = stemmer.stem(input)
        return hasil

    def sinonim(self,input):
        keyword_processor = KeywordProcessor()
        keyword_dict = {
            "kerja praktik":["kp","magang"],
            "skripsi":["ta","tugas akhir"],
            "syarat":["tentu"],
            "kampus merdeka":["mbkm","msib"],
            "cumlaude":["pujian"],
            "sop":["cara","kriteria","langkah","alur"],
            "tanda tangan":["ttd"],
            "ketua jurusan":["kajur"],
            "mata kuliah":["mk"],
            "desk evaluation":["de","sempro","seminar proposal","sidang proposal","sidang sempro"],
            "komprehensif":["kompre", "sidang kompre", "ujian kompre", "sidang skripsi","sidang ta"],
            "stop out":["so"],
            "drop out":["do","putus studi"],
            "panduan":["format","penulisan","format penulisan"],
            "suliet":["toefl","usept"],
            "pembimbing skripsi":["dosbing","bimbing proposal"],
            "khs":["kartu hasil studi"],
            "form":["formulir"],
            "simak":["sistem akademik"],
            "krs":["krsnya"],
            "serah":["kumpul"],
            "telat":["lewat"],
            "ambil":["isi"],
            "aktif":["masih"],
            "teknik informatika":["ti"],
            "krs":["kartu rencana studi","kartu studi mahasiswa","ksm"],
            "perlu":["urus"],
            }
        keyword_processor.add_keywords_from_dict(keyword_dict)
        hasil = keyword_processor.replace_keywords(input)
        return hasil

    def konversi_ascii(self,input):
        hasil_konversi_inputan = []
        i=0
        while i < len(input):
            j=0
            pow = 1
            ascii = []
            while j < len(input[i]):
                convert = ord(input[i][j])
                hash = convert * math.pow(26,pow)
                ascii.append(hash)
                j = j + 1
                pow = pow - 1
            hasil_konversi_inputan.append(ascii)
            i = i+1
        return hasil_konversi_inputan

    def rolling_hash(self,input):
        hasil_hashing = []
        i=0
        while i < len(input):
            j=0
            while j < len(input[i]):
                tambah = int(input[i][j] + input[i][j+1])
                hasil_hashing.append(tambah)
                j = j + 2
            i = i+1
        return hasil_hashing

    def truncate(self,num, n):
            integer = int(num * (10**n))/(10**n)
            return float(integer)

    def irisan(self,lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        
        return lst3