import os
import json

from tqdm import tqdm


if __name__ == "__main__":
    print('=== 양봉 데이터 JSON 파일 커스텀 코드 (START) ==================================')

    root_path = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(root_path, '양봉_output_20221116')

    new_json_path = os.path.join(root_path, '양봉_NEW_1227')

    print(json_path)

    list_type_folder = os.listdir(json_path)        # 구분 (실제데이터, 파괴데이터) >> (생애주기, 생애이슈)

    list_farm_name = {'01': '곤충잠업연구소', 
                      '02': '국립농업과학원', 
                      '03': '꿀벌테마파크', 
                      '04': '휴먼앤허나비', 
                      '05': '한국양봉협회', 
                      '06': '전남바이오산업진흥원'}

    for type_folder in list_type_folder:
        
        bee_type = '생애주기'                       # 생애별 분류 키값

        print(type_folder)

        if type_folder == '실제데이터':
            bee_type = '생애주기'
        else:
            bee_type = '생애이슈'

        path_sub_01 = os.path.join(json_path, type_folder)

        list_labeling_folder = os.listdir(path_sub_01)

        for labeling_folder in list_labeling_folder:
            
            # 생애 단계별 분포
            path_sub_02 = os.path.join(path_sub_01, labeling_folder)

            list_lifecycle_folder = os.listdir(path_sub_02)     

            for lifecycle_folder in list_lifecycle_folder:
                
                print(lifecycle_folder)
                lifecycle_name = lifecycle_folder.split('.', 2)[1]

                path_sub_03 = os.path.join(path_sub_02, lifecycle_folder)

                list_json_file = os.listdir(path_sub_03)

                for one_json in tqdm(list_json_file):
                    
                    list_split_name = one_json.split('_')
                    farm_num = list_split_name[0]
                    species_en = list_split_name[4]

                    species_ko = '종 구분 없음'

                    if species_en == 'LI':
                        species_ko = '이탈리안'
                    elif species_en == 'CA':
                        species_ko = '카니올란'
                    elif species_en == 'AP':
                        species_ko = '한봉'
                    elif species_en == 'BI':
                        species_ko = '호박벌'
                    else:
                        species_ko = '종 구분 없음'

                    farm_name = list_farm_name[farm_num]

                    file_path = os.path.join(path_sub_03, one_json)
                    json_data = ''

                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)

                    list_new_annotation = []

                    list_orgin_annotaion = json_data['ANNOTATION_INFO']

                    for one in list_orgin_annotaion:
                        
                        one['FARM'] = farm_name
                        one['LIFE_CLASS'] = bee_type
                        one['SPECIES'] = species_ko
                        one['LIFECYCLE'] = lifecycle_name

                        list_new_annotation.append(one)

                    json_data['ANNOTATION_INFO'] = list_new_annotation


                    save_json_path = os.path.join(new_json_path, '커스텀', bee_type, labeling_folder, lifecycle_folder)
                
                    if not os.path.exists(save_json_path):
                        os.makedirs(save_json_path)

                    with open(save_json_path + '/' + one_json, "w", encoding='utf8') as fp:
                        fp.write(json.dumps(json_data, ensure_ascii=False, default=str, indent='\t'))
                        
    print('=== 양봉 데이터 JSON 파일 커스텀 코드 (SUCCESS) ===============================')
    print('=============================================================================')

