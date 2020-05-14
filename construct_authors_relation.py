import pickle
import argparse
import os
from collections import Counter, defaultdict

from utils import read_qts, get_alter_names_from_CBDB

def get_alter_names(qts_file, cbdb_file, save_dir):
  alter_names_file = os.path.join(save_dir, "alternames.pkl")

  if os.path.exists(alter_names_file):
    print("find dumped alternames file, loading directly.")
    with open(alter_names_file, 'rb') as f:
      qts_list, authors_filtered_by_CBDB, alter_names_dict = pickle.load(f)
  else:
    print("processing QuanSongCi...")
    # 读取全宋词，并存储诗歌内容和作者
    qts_list, authors_set = read_qts(qts_file)
    # 删除部分作者
    authors_set -= mannual_deleted_authors

    alter_names_dict, authors_filtered_by_CBDB = get_alter_names_from_CBDB(cbdb_file, authors_set,
                                                                           manual_defuzzy_authors_id)
    # 刪除不想要的別稱
    for k, v in mannual_deleted_alter_names.items():
      alter_names_dict[k] -= v
    # 補充CBDB中缺少的別稱
    for k, v in mannual_added_alter_names.items():
      alter_names_dict[k] |= v

    # 存储计算结果
    with open(alter_names_file, 'wb') as f:
      pickle.dump([qts_list, authors_filtered_by_CBDB, alter_names_dict], f)

  return qts_list, authors_filtered_by_CBDB, alter_names_dict


def get_refer_relations(qts_list, authors_filtered_by_CBDB, alter_names_dict, save_dir):
  reference_relations_file = os.path.join(save_dir, 'reference_relations.pkl')

  if os.path.exists(reference_relations_file):
    print("find dumped reference relations file, skip calculating.")
    return
  else:
    print("calculating reference relations...")
    reference_relations_counter = Counter()
    reference_relations_text = defaultdict(list)
    # 逐个作者搜寻
    for name in authors_filtered_by_CBDB:
      # 逐首诗搜寻
      for author, title, text in qts_list:
        # 如果不在CBDB过滤过的set中，直接跳过
        if author not in authors_filtered_by_CBDB:
          continue

        poem = title + ' ' + text
        # 查找本名，标题加正文中只要出现一次名字就可以
        if poem.find(name) != -1:
          reference_relations_counter[(author, name)] += 1
          reference_relations_text[(author, name)].append(title)
          continue
        # 查找别名
        alt_names = alter_names_dict[name]
        for alt_name in alt_names:
          if poem.find(alt_name) != -1:
            reference_relations_counter[(author, name)] += 1
            reference_relations_text[(author, name)].append(title)
            break
    # 存储计算结果
    with open(reference_relations_file, 'wb') as f:
      pickle.dump([reference_relations_counter, reference_relations_text], f)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--works_path', type=str, default='source/song.txt',
                      help='file path of Quan Tangshi')
  parser.add_argument('--cbdb_path', type=str, default='source/cbdb_sqlite.db',
                      help='file path of CBDB')
  parser.add_argument('--save_dir', type=str, default='data',
                      help='directory to pickle intermediate data')
  args = parser.parse_args()

  # 检查存储目录是否存在
  if not os.path.isdir(args.save_dir):
    os.makedirs(args.save_dir)

  qts_list, authors_filtered_by_CBDB, alter_names_dict = get_alter_names(args.works_path, args.cbdb_path, args.save_dir)
  get_refer_relations(qts_list, authors_filtered_by_CBDB, alter_names_dict, args.save_dir)


if __name__ == '__main__':
  main()

