import time

__author__ = 'zz'

from core.engine import Engine


def shell_main():
    print("""
    输入 url， 响应数， 最大搜索页数， 空格隔开, 回车结束一次输入
    比如\n
    http://h.nimingban.com/f/%E7%BB%BC%E5%90%88%E7%89%881 20 10\n
    连续两次回车开始程序
    """)
    tasks = []
    while True:
        ip = input()
        if not ip:
            break

        url, response_gt, max_page = ip.split()
        tasks.append({
            'url': url,
            'response_gt': int(response_gt),
            'max_page': int(max_page),
        })
    engine = Engine()
    engine.set_init_tasks(tasks)
    engine.start()

    print('-----------Engine Start----------')

    while engine.is_running:
        rs = engine.get_one_result()
        if not rs:
            time.sleep(0.5)
            continue
        print(rs.link, 'image', rs.image_url or 'None')
        print(rs.text)
        print('-'*40)

    print('------------Engine Stop---------------')

def main():
    from gui.main import root
    root.mainloop()

if __name__ == '__main__':
    shell_main()
