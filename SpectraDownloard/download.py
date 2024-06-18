import multiprocessing
import sys, os

sys.path.append(os.path.join(sys.path[0], '..'))
from SpectraDownloard.lamost import lamost


def a(num,lm,url):
    lm.downloadFits(obsid=str(url), savedir='D:\综述实验2\关联规则\验证所需光谱/')
    print('下载了{}个光谱'.format(num))

def main():
    lm = lamost()
    lm.dataset = 8
    lm.version = float(2.0)
    # lm.version = int(0)
    lm.token = 'F0082ce863c'
    # lm.token = 'F27eb78f7a0'
    # lm.token = None


    # 使用方法：
    num = 0  # 计数

    # print("总cpu数:",multiprocessing.cpu_count())
    all_cpu = multiprocessing.cpu_count()  # 全部cpu执行 cpuNum:8
    pool = multiprocessing.Pool(2) # 两个进程执行
    # pool = multiprocessing.Pool(all_cpu - 2)


    with open('D:\BrowserDownload/url-1701833212343.txt', 'r') as f:
        for url in f:
            # 下面两行是下载网页所有光谱需要用到的格式
            url = url.replace('http://www.lamost.org:80/dr8/v2.0/spectrum/fits/', '')
            url = url.replace('?token=F0082ce863c\n', '')

            # 下载fits文件
            # url=url.replace('\n','')
            num += 1
            # 并行下载
            pool.apply_async(func=a,args=(num,lm,url))
            # lm.downloadFits(obsid=str(url), savedir='D:/实验数据集/光谱/A1高信噪比恒星光谱')
            # print('下载了{}个光谱'.format(num))


            # print('下载了{}个光谱'.format(num))
        pool.close()
        pool.join()
        f.close()

if __name__ == '__main__':
    main()
