from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def get_provider_info(phone_number):
    # Hapus semua spasi dan karakter non-angka
    cleaned_number = re.sub(r'\D', '', phone_number)
    
    # Jika nomor dimulai dengan '+62', ubah ke format '0'
    if cleaned_number.startswith('62'):
        cleaned_number = '0' + cleaned_number[2:]
    
    # Jika tidak dimulai dengan '0', tambahkan
    if not cleaned_number.startswith('0'):
        cleaned_number = '0' + cleaned_number
    
    # Periksa panjang nomor
    length = len(cleaned_number)
    
    # Cek 4 digit pertama untuk menentukan provider
    prefix = None
    if len(cleaned_number) >= 4:
        prefix = cleaned_number[:4]
    
    result = {
        'nomor': cleaned_number,
        'valid': False,
        'provider': 'Tidak dikenal',
        'jenis_kartu': 'Tidak dikenal',
        'panjang': length,
        'prefix': prefix,
        'keterangan': ''
    }
    
    # Validasi format dasar nomor telepon Indonesia
    if not cleaned_number.startswith('0') or length < 10 or length > 12:
        result['keterangan'] = 'Nomor telepon tidak valid. Nomor harus 10-12 digit dan dimulai dengan 0.'
        return result
    
    # Periksa provider berdasarkan awalan
    # Telkomsel
    if prefix in ['0811']:
        result['provider'] = 'Telkomsel'
        result['jenis_kartu'] = 'Kartu Halo (Pascabayar)'
        result['valid'] = 10 <= length <= 12
    elif prefix in ['0812', '0813']:
        result['provider'] = 'Telkomsel'
        result['jenis_kartu'] = 'Kartu Halo atau Simpati'
        result['valid'] = 10 <= length <= 12
    elif prefix in ['0821', '0822']:
        result['provider'] = 'Telkomsel'
        result['jenis_kartu'] = 'Kartu Simpati'
        result['valid'] = 10 <= length <= 12
    elif prefix in ['0823', '0852', '0853']:
        result['provider'] = 'Telkomsel'
        result['jenis_kartu'] = 'Kartu AS'
        result['valid'] = 10 <= length <= 12
    elif prefix in ['0851']:
        result['provider'] = 'Telkomsel'
        result['jenis_kartu'] = 'Kartu AS atau By.U'
        result['valid'] = 10 <= length <= 12
    
    # Indosat
    elif prefix in ['0855']:
        result['provider'] = 'Indosat'
        result['jenis_kartu'] = 'Matrix'
        result['valid'] = length == 10
    elif prefix in ['0856', '0857']:
        result['provider'] = 'Indosat'
        result['jenis_kartu'] = 'IM3'
        result['valid'] = length == 10 or length == 11 or length == 12
    elif prefix in ['0858']:
        result['provider'] = 'Indosat'
        result['jenis_kartu'] = 'Mentari'
        result['valid'] = length == 12
    elif prefix in ['0814']:
        result['provider'] = 'Indosat'
        result['jenis_kartu'] = 'Indosat M2'
        result['valid'] = length == 12
    elif prefix in ['0815']:
        result['provider'] = 'Indosat'
        result['jenis_kartu'] = 'Matrix, Mentari'
        result['valid'] = length == 11 or length == 12
    elif prefix in ['0816']:
        result['provider'] = 'Indosat'
        result['jenis_kartu'] = 'Matrix, Mentari'
        result['valid'] = length == 10 or length == 11 or length == 12
    
    # Tri
    elif cleaned_number.startswith('0895') or cleaned_number.startswith('0896') or \
         cleaned_number.startswith('0897') or cleaned_number.startswith('0898') or \
         cleaned_number.startswith('0899'):
        result['provider'] = 'Tri'
        result['jenis_kartu'] = 'Tri'
        result['valid'] = 10 <= length <= 12
    
    # XL Axiata
    elif prefix in ['0817', '0818', '0819']:
        result['provider'] = 'XL Axiata'
        result['jenis_kartu'] = 'Pra bayar dan Explor'
        result['valid'] = length == 10 or length == 11 or length == 12
    elif prefix in ['0859', '0877', '0878']:
        result['provider'] = 'XL Axiata'
        result['jenis_kartu'] = 'Pra bayar dan Explor'
        result['valid'] = length == 12

    # AXIS
    elif cleaned_number.startswith('0831') or cleaned_number.startswith('0832') or \
         cleaned_number.startswith('0833') or cleaned_number.startswith('0838'):
        result['provider'] = 'AXIS'
        result['jenis_kartu'] = 'AXIS'
        result['valid'] = 10 <= length <= 12
    
    # Smartfren
    elif cleaned_number.startswith('0881') or cleaned_number.startswith('0882') or \
         cleaned_number.startswith('0883') or cleaned_number.startswith('0884') or \
         cleaned_number.startswith('0885') or cleaned_number.startswith('0886') or \
         cleaned_number.startswith('0887') or cleaned_number.startswith('0888') or \
         cleaned_number.startswith('0889'):
        result['provider'] = 'Smartfren'
        result['jenis_kartu'] = 'Smartfren'
        result['valid'] = length == 11 or length == 12
    
    if not result['valid'] and result['provider'] != 'Tidak dikenal':
        result['keterangan'] = f"Panjang nomor tidak sesuai untuk provider {result['provider']}."
    elif result['valid']:
        result['keterangan'] = f"Nomor valid untuk provider {result['provider']}."
    
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cek-nomor', methods=['POST'])
def cek_nomor():
    data = request.get_json()
    nomor = data.get('nomor', '')
    
    result = get_provider_info(nomor)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
