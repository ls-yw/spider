#coding:UTF8
'''
@author: linsen
'''



class HtmlOutputer(object):
    def __init__(self):
        self.datas = []
    
    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    
    def output_html(self):
        fout = open('output.html', 'w')
        
        fout.write('<html>')
        fout.write('<bodey>')
        fout.write('<table>')
        
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%</td>'% data['url'])
            fout.write('<td>%</td>'% data['title'].encode('utf-8'))
            fout.write('<td>%</td>'% data['summary'].encode('utf-8'))
            fout.write('</tr>')
        
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
    
    
    
    



