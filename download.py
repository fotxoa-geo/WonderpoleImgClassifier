import os
import pickle
import requests
from zerionPy import IFB
import json

f = open('configs.json')
data = json.load(f)
metadata = data['keys']  # geodata from spec library

ck = metadata['ck']
sk = metadata['cs']
server_name = metadata['server_name']
profile_id = metadata["profile_id"]
emit_transects_page_id = metadata["emit_transects_page_id"]


def save_pickle(object, filename):
    with open(os.path.join('objects', filename + '.pickle'), 'wb') as handle:
        pickle.dump(object, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(filename):
    with open(os.path.join('objects', filename + '.pickle'), 'rb') as handle:
        b = pickle.load(handle)
        return b


def get_iform_records(server_name:str, client_key:str, secret_key:str, profile_id:int, page_id: int):
    api = IFB(server_name, 'us', client_key, secret_key, 6)
    results = api.getRecords(profile_id, page_id).response

    print("downloading... ", len(results), " records")
    records = []
    for i in results:
        data = api.getRecord(profile_id, page_id, i['id']).response
        records.append(dict(list(data.items())[14:]))

    return records


def download_emit_sites():
    # the transect spectra - of
    records = load_pickle('emit_slpit')

    print("loading... Spectral Transects")
    for i in records:
        plot_name = f"{i['team_names'].capitalize()} - {i['plot_num']:03d}"
        plot_pic_url = i['landscape_pic']
        date = i['sample_date']
        plot_measurements = i['plot_measurements'].split(",")

        if 'wonderpole' not in plot_measurements:
            print(plot_measurements)
            print(i)
            continue

        print(f'\t loading... {plot_name}')

        img_data = requests.get(plot_pic_url).content
        with open(os.path.join('plot_landscape', f"{plot_name}.jpg"), 'wb') as handler:
            handler.write(img_data)

    print("successfully downloaded data...")


def run_dowloand_slpit():
    emit_slpit_recrods = get_iform_records(server_name=server_name, client_key=ck, secret_key=sk,
                                           profile_id=profile_id, page_id=emit_transects_page_id)
    save_pickle(emit_slpit_recrods, 'emit_slpit')
    download_emit_sites()

