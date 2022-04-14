from src import EAF2IGT, IGT
import pprint as pp

def main():
  obj = EAF2IGT("tests/data/BEJ_MV_CONV_01_RICH.EAF")
  #pp.pprint(obj.paragraphs)
  igt = obj.get_igt()
  igt.to_emeld("tests/data/test.emeld", ["source"], ["speaker"], ["ft", "participant", "id"], [], ["txt", "gls", "id"])

if __name__ == '__main__':
    main()

