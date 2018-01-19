#encoding:utf-8

#导入Tkinter模块
from Tkinter import  *
import Tkinter
from ttk import *
import platform
import tkFont
import tkFileDialog
import tkMessageBox

class UI(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master=master
        self.rowdis=5
        self.coldis=5
        self.initrow=5
        self.initcol=5
        self.OS = platform.system().lower()
        self.debug = False
        #self.num=StringVar()
        #实体标签
        self.label=['B','I','O']
        self.pos_label=['Nh','Ns','Ni','Ne','Na','Nt','Nm']
		#用于存储撤销信息
        self.backdict={}
		
        #参考实体信息
        self.entities = [
            u"人名", u"地名", u"机构名", u"装备名", u"事件名", u"时间", u"数量"
        ]
        self.entityinfo={
            self.entities[0]:u"人名：张三，李四，王五，麻六等",
            self.entities[1]:u"地点名：郑州市，北京市，青岛市，杭州市，郑东新区等",
            self.entities[2]: u"组织名：郑州大学，国务院，新华社等",
            self.entities[3]: u"装备名：歼-20，歼-10、歼-11，PL-21导弹，346型相控阵雷达等",
            self.entities[4]: u"事件名：暂不进行标注等",
            self.entities[5]: u"时间：7月8日等",
            self.entities[6]: u"数量：76%，等"
        }
        #颜色信息
        self.color=['red','yellow','blue','green','brown','orange','purple']
        self.color_index=['a','b','c','d','e','f','g']

        #存储读入文件信息
        self.filename=''
        self.file_buff=[]
        self.buff_action=[]  #备份文件内容，可用于撤销，以防万一等操作
        self.ann_buff=[]  #存储已标注文本
        self.index=0
        #进行标注
        self.leftAction_flag=False
        self.flag=False
        self.firstSelection_index=''
        self.cursor_index=''
        self.position=[]   #存储所有已经选择的位置
        self.position_flag=False #位置标志位
        self.position_b_e={} #存储所有需要标记的实体开始，结束位置，用字典进行标记，其中，key为顺序，value分别存储实体位置以及实体类型
        self.text_before=''
        self.text_cursor=''
        self.text_after=''
        self.back=[]  #主要用来支持撤销操作

        self.initUI()

    def initUI(self):
        # self.master.title("命名实体人工标注工具V1.0")
        # self.pack(fill=BOTH, expand=True)
        #首先定义文本显示框
        self.label=Label(self.master,font=(None,15,"bold"),text="需要实体标注的文本：")
        self.label.grid(row=0,column=0,columnspan=5,rowspan=1)
        self.label1 = Label(self.master, font=(None, 10,"bold"))
        self.label1.grid(row=0,column=3,columnspan=100,rowspan=1)

        self.text=Text(self.master,font=(None,15),width=100,height=15)
        self.text.grid(row=2,column=1,columnspan=30,rowspan=30,ipadx=2,ipady=2,padx=2,pady=2)#,sticky=N+S+E+W)

        self.button_import = Button(self.master, text="导入文件",command=self.open_file)
        self.button_import.grid(row=2, column=35)
        self.button_export = Button(self.master, text="导出文件",command=self.export_file)
        self.button_export.grid(row=4, column=35)
        self.button_save=Button(self.master,text="顺序撤销",command=self.back_order)
        self.button_save.grid(row=6,column=35)
        self.button_back = Button(self.master, text="选择撤销",command=self.back_random)
        self.button_back.grid(row=8, column=35)
        self.button_next=Button(self.master,text="上一句",command=self.fore_button)
        self.button_next.grid(row=10,column=35)
        self.button_fore=Button(self.master,text="下一句",command=self.next_button)
        self.button_fore.grid(row=12,column=35)
        self.sum_label1=Label(self.master, font=(None, 10,"bold"),text="总句数：(条)")
        self.sum_label1.grid(row=14,column=35)
        self.text_sum=Text(self.master, font=(None, 15),width=5,height=1)
        self.text_sum.grid(row=16,column=35)
        self.sum_label3=Label(self.master, font=(None, 10,"bold"),text="剩余句数：(条)")
        self.sum_label3.grid(row=18,column=35)
        self.text_ret=Text(self.master, font=(None, 15),width=5,height=1)
        self.text_ret.grid(row=20,column=35)
     
		

        #实体类型, E 右对齐，W 左对齐，
        self.label = Label(self.master,font=(None,15,"bold"), text="实体类型选择：")
        self.label.grid(columnspan=3,rowspan=1,sticky=N+W)

        self.button1=Button(self.master,text=u"A:"+self.entities[0],width=15,command=self.button_people)
        self.button1.grid(row=45,column=2,sticky=N+E )
        self.button2 = Button(self.master, text=u"B:"+self.entities[1],width=15,command=self.button_place)
        self.button2.grid(row=45, column=4, sticky=N)
        self.button3 = Button(self.master, text=u"C:"+self.entities[2],width=15,command=self.button_organize)
        self.button3.grid(row=45, column=6, sticky=N)
        self.button4 = Button(self.master, text=u"D:"+self.entities[3],width=15,command=self.button_time)
        self.button4.grid(row=45, column=8, sticky=N)
        self.button5 = Button(self.master, text=u"E:"+self.entities[4],width=15,command=self.button_date)
        self.button5.grid(row=45, column=10, sticky=N)
        self.button6 = Button(self.master, text=u"F:"+self.entities[5],width=15,command=self.button_number)
        self.button6.grid(row=45, column=12, sticky=N)
        self.button7 = Button(self.master, text=u"G:"+self.entities[6],width=15,command=self.button_percege)
        self.button7.grid(row=45, column=14, sticky=N)
        #实体类型参考：
        self.label = Label(self.master,font=(None,15,"bold"), text="实体类型说明：")
        self.label.grid(columnspan=3,rowspan=1,sticky=N+W)
        # self.var = StringVar()
        # self.lb = Listbox(self.master, width=80, height=12, selectmode=BROWSE, font=("Arial", 10), listvariable=self.var)
        # # self.lb.bind('<ButtonRelease-1>',self.print_item)
        # self.lb.grid(row=47,column=1)
        # self.lb.bind('<Double-Button-1>', self.print_item)
        self.text1 = Text(self.master, font=(None,15,"bold"),width=100, height=10)
        # self.text1.grid(row=47,column=1)
        self.text1.grid(row=47, column=2, columnspan=30, rowspan=30, ipadx=2, ipady=2, padx=2, pady=2)  # ,sticky=N+S+E+W)
        # self.label2 = Label(self.master, text="软件说明：\n")
        # self.label2.grid(row=2, column=38)

        # self.label1=Label(self.master,text="first").grid(row=0,column=0)
        # self.label2=Label(self.master,text="secong").grid(row=1,column=0)
        # e1=Entry(self.master).grid(row=1,column=12)
        # e2=Entry(self.master).grid(row=2,column=12)
        self.text.bind("<B1-Motion>",self.leftAction)
        for col_ind,col in zip(self.color_index,self.color):
            self.text.tag_config(col_ind, background="white", foreground=col)
            self.text1.tag_config(col_ind, background="white", foreground=col)
        # self.text.tag_config('b', background="white", foreground="yellow")
        # self.text.tag_config('c', background="white", foreground="blue")
        # self.text.tag_config('d', background="white", foreground="green")
        # self.text.tag_config('e', background="white", foreground="black")
        # self.text.tag_config('f', background="white", foreground="orange")
        # self.text.tag_config('g', background="white", foreground="purple")
        self.text.bind('<Control-Key-z>', self.back_order)
        self.text.bind('<Control-Key-a>', self.key_button_people)
        self.text.bind('<Control-Key-b>', self.key_button_place)
        self.text.bind('<Control-Key-c>', self.key_button_organize)
        self.text.bind('<Control-Key-d>', self.key_button_time)
        self.text.bind('<Control-Key-e>', self.key_button_date)
        self.text.bind('<Control-Key-f>', self.key_button_number)
        self.text.bind('<Control-Key-g>', self.key_button_percege)
        self.text.bind('<Control-Key-s>', self.export_file)
		
        #self.text.bind('', self.textReturnEnter)
    def back_order(self):
		sent=self.text.get(0.0,END)
		num_buff=add_color(sent)
		if len(num_buff)>0:
			ind=num_buff[-1]
			ind1=int(ind[0].split('.')[1])
			ind2=int(ind[1].split('.')[1])
			word=sent[ind1:ind2]
			word=word[word.index('[@')+2:word.index('#')]
			self.text.delete(ind[0],ind[1])
			self.text.insert(ind[0],word)
		else:
			pass
		
    def back_random(self):
		sent=self.text.get(0.0,END)
		num_buff=add_color(sent)
		if len(num_buff)>0:
			current_location=self.text.index(SEL_LAST)
			#print current_location
			num_current=int(current_location.split('.')[1])
			for ind in num_buff:
				ind1=int(ind[0].split('.')[1])
				ind2=int(ind[1].split('.')[1])
				if ind1<=num_current<ind2:
					word=sent[ind1:ind2]
					word=word[word.index('[@')+2:word.index('#')]
					self.text.delete(ind[0],ind[1])
					self.text.insert(ind[0],word)
					break
		else:
			pass
				
			
		

    #对导入的文件进行处理
    def prepro(self,line,num):
		s=''
		data=cutthree(line)
		#print data[0]
		#print data[1]
		#print data[2]
		buff=likecrf(data[1])
		#print buff
		flag=False
		sent=''
		ind_buff=[]
		for i,w in enumerate(data[0]):
		
			for j,ind in enumerate(buff):
			
				if ind[0]<=i<ind[1]:
					flag=True
					if j not in ind_buff:
						#sent+=' '.join(list(data[0][i:]))
						s=s+u'[@' + ' '.join(data[0][ind[0]:ind[1]]) + u'#' + self.entities[self.pos_label.index(data[2][ind[0]])] + u'*]'+u' '
						self.backdict[num].append([sent+' '.join(list(data[0][i:])),'1.'+str(len(sent)),u'[@' + ' '.join(data[0][ind[0]:ind[1]]) + u'#' + 
													self.entities[self.pos_label.index(data[2][ind[0]])] + u'*]'+u' '])
						ind_buff.append(j)
						sent=s
						#print sent
						
					break
				else:
					pass
			if flag==True:
				flag=False
				pass
			else:
				s+=u' '+w+u' '
				flag=False
				sent=s
		return s					

        #self.text.bind("")

    # 百分比
    def key_button_percege(self,event):
        self.choose_action(self.entities[6], self.color_index[6])

    # 数字
    def key_button_number(self,event):
        self.choose_action(self.entities[5], self.color_index[5])

    # 日期
    def key_button_date(self,event):
        self.choose_action(self.entities[4], self.color_index[4])

    # 时间
    def key_button_time(self,event):
        self.choose_action(self.entities[3], self.color_index[3])

    # 机构名
    def key_button_organize(self,event):
        self.choose_action(self.entities[2], self.color_index[2])

    # 地名
    def key_button_place(self,event):
        self.choose_action(self.entities[1], self.color_index[1])

    # 人名
    def key_button_people(self,event):
        self.choose_action(self.entities[0], self.color_index[0])
    #撤销操作
    def back_action(self):
	'''
	    if len(self.backdict[self.index])==0:
            print self.text.get(0.0, END)
        else:
            print self.text.get(0.0,END)
            tmp=self.backdict[self.index][-1]
            self.backdict[self.index]=self.backdict[self.index][:-1]
            self.text.delete(tmp[1],u'1.'+str(int(tmp[1].split('.')[-1])+len(tmp[-1])))
            self.text.insert(tmp[1],tmp[-1][2:tmp[-1].index('#')])
		
	'''
        #print len(self.backdict[self.index])
        #print self.index
        if len(self.backdict[self.index])==0:
            #print self.text.get(0.0, END)
            pass
        else:
            #print self.text.get(0.0,END)
            tmp=self.backdict[self.index][-1]
            #print tmp[0],'\n',tmp[1],'\n',tmp[2]
            self.backdict[self.index]=self.backdict[self.index][:-1]
            self.text.delete(tmp[1],u'1.'+str(int(tmp[1].split('.')[-1])+len(tmp[-1])))
            self.text.insert(tmp[1],tmp[-1][2:tmp[-1].index('#')])
    ##################################################
    '''对文本框中的内容进行标注，实体标注，可快捷键标注，可以点击按钮进行标注'''
    # 百分比
    def button_percege(self):
        self.choose_action(self.entities[6], self.color_index[6])
    #数字
    def button_number(self):
        self.choose_action(self.entities[5],self.color_index[5])
    #日期
    def button_date(self):
        self.choose_action(self.entities[4],self.color_index[4])
    #时间
    def button_time(self):
        self.choose_action(self.entities[3],self.color_index[3])
    #机构名
    def button_organize(self):
        self.choose_action(self.entities[2],self.color_index[2])
    #地名
    def button_place(self):
        self.choose_action(self.entities[1],self.color_index[1])
    #人名
    def button_people(self):
        self.choose_action(self.entities[0],self.color_index[0])
    #选择标注操作
    def choose_action(self,entity,color):
        self.button_entity_action()
        self.text.delete(self.firstSelection_index, self.cursor_index)
        self.text.insert(self.firstSelection_index, u'[@' + self.text_cursor + u'#' + entity + u'*]', color)
        #print self.firstSelection_index
        self.backdict[self.index].append([self.text.get(0.0, END), self.firstSelection_index,
                         u'[@' + self.text_cursor + u'#' + entity + u'*]'])
		#self.backdict[self.index].append([self.text.get(0.0, END), self.firstSelection_index,
        #                  u'[@' + self.text_cursor + u'#' + entity + u'*]'])
    #鼠标选择操作
    def button_entity_action(self):
        self.flag_sel()
        if self.flag and self.leftAction_flag:
            self.firstSelection_index = self.text.index(SEL_FIRST)
            self.cursor_index = self.text.index(SEL_LAST)
            #print self.firstSelection_index, self.cursor_index
            self.text_before=self.text.get(1.0,self.firstSelection_index)
            self.text_cursor=self.text.get(self.firstSelection_index,self.cursor_index)
            self.text_after=self.text.get(self.cursor_index,END)
            self.flag = False
            self.leftAction_flag=False
        else:
            pass
    #鼠标选择标志
    def flag_sel(self):
        try:
            self.firstSelection_index = self.text.index(SEL_FIRST)
            self.cursor_index = self.text.index(SEL_LAST)
        except:
            self.flag=False
        else:
            self.flag=True
    def leftAction(self,event):
        self.leftAction_flag=True
		
	

    ##################################################
	'''
	#对显示的文本进行加色处理
	def add_color(self,line):
		num_buff=[]
		if '[@' not in line:
			pass
		else:
			tmp=line.split('[@')
			num=0
			start=0
			end=0
			for w in tmp:
				start=num
				end=num+len('[@')+w.index('*]')+2
				entity=w[w.index('#')+1:w.index('*]')]
				num_buff.append([start,end,entity])
		return num_buff
	'''
	
	
	
	
    #将文件内容在文本框显示出来
    def display(self):
        self.text.delete(1.0, Tkinter.END)
        self.text.insert(END, self.ann_buff[self.index])
        #num_buff=self.add_color(self.ann_buff[self.index])
        num_buff=add_color(self.ann_buff[self.index])
        if len(num_buff)>0:
			for ind in num_buff:
				self.text.tag_add(self.color_index[self.entities.index(ind[2])],ind[0],ind[1])
		
    #导出文件
    def export_file(self):
        with open(self.filename+'ann.txt','w') as f_w:
            for line in self.ann_buff:
                f_w.write(self.process_line(line).encode('utf-8')+'\n')
            #f_w.write('\n'.join(self.file_buff).encode('utf-8'))
     #上一句
    def fore_button(self):
        self.ann_buff[self.index]=self.text.get(0.0,END)
        if self.index>0:
            self.index-=1
            self.display()
            if self.index%10==0:
				self.export_file()
            self.text_ret.delete(1.0, Tkinter.END)
            self.text_ret.insert(END,len(self.file_buff)-self.index)
        else:
            tkMessageBox.showinfo("警告！", "已经到第一句，请继续标注下一句或者导出文件！")
    #下一句
    def next_button(self):
        #print self.process_line(self.text.get(0.0,END))
        self.ann_buff[self.index]=self.text.get(0.0,END)
        #self.file_buff[self.index]=self.text.get(0.0,END)
        if self.index<len(self.file_buff):
            self.index+=1
            self.display()
            if self.index%10==0:
				self.export_file()
            if self.index==len(self.file_buff)-1:
				self.export_file()
            self.text_ret.delete(1.0, Tkinter.END)
            self.text_ret.insert(END,len(self.file_buff)-self.index)
			
        else:
            tkMessageBox.showinfo("警告！", "已经到最后一句，请继续标注上一句或者导出文件！")

    def info_display(self):
        self.text1.delete(1.0, Tkinter.END)
        for color in self.color_index:
            self.text1.insert(END,self.entities[self.color_index.index(color)]+'\t\t'+self.entityinfo[self.entities[self.					color_index.index(color)]]+'\n',color)
			
			
			
    '''响应导入文件按钮，选择需要标注的文件，并进行读取，同时将文本路径显示在窗口顶端，将文本第一行导入文本框'''
    def open_file(self):
        ftypes = [('all files', '.*'), ('text files', '.txt')]
        dlg = tkFileDialog.Open(self, filetypes=ftypes)
        fl = dlg.show()
        if fl != '':
            self.text.delete("1.0", END)
            self.readFile(fl)
            self.ann_buff=self.file_buff
            self.display()
            self.info_display()
            self.index=0
            self.filename=fl
            #self.text.insert(END, text)
            #print chardet.detect(fl).items()
            labe_name=u"标注文件为:"+fl
            self.label1.config(text=labe_name)
            # #self.setNameLabel("File: " + fl)
            # #self.setDisplay()
            # # self.initAnnotate()
            # self.text.mark_set(INSERT, "1.0")
            # self.setCursorLabel(self.text.index(INSERT))
    #读取需要进行实体标注的文件，并以列表形式存储
    def readFile(self,src):
        num=0
        self.file_buff=[]
        with open(src,'r') as f_r:
            for line in f_r:
                #line=line.strip().decode(chardet.detect(line)['encoding'])
                line=line.strip().decode('utf-8')
                if line:
					#self.backdict[num]=[]
                    self.backdict[num]=[]
                    self.file_buff.append(self.prepro(line,num))
                    num+=1
            self.text_sum.delete(1.0, Tkinter.END)
            self.text_sum.insert(END,len(self.file_buff))
            self.index=0
            self.text_ret.delete(1.0, Tkinter.END)
            self.text_ret.insert(END,len(self.file_buff)-self.index)
        pass
        #print len(self.file_buff)
    #将标注过的文本转化成标签形式
    def process_line(self,line):
        s=''
        if u'*]' in line:
            sent_tmp=line.split(u'*]')
            for sent in sent_tmp:
                if u'[@' in sent:
                    w_tmp=sent.split(u'[@')
                    if ' ' in w_tmp[0].strip():
                        s+=u'/O '.join(w_tmp[0].split())+u'/O '
                    elif w_tmp[0].strip():
                        s+=w_tmp[0].strip()+u'/O'+u' '
                    else:
                        pass
                    #print w_tmp[1]
                    ind=w_tmp[1].index(u'#')
                    label=self.pos_label[self.entities.index(w_tmp[1][ind+1:])]
                    s1=w_tmp[1][:ind]
                    if ' ' in s1.strip():
                        s_tmp=s1.split()
                        s+=s_tmp[0]+u'/B-'+label+u' '
                        s+=(u'/I-'+label+u' ').join(s_tmp[1:])+u'/I-'+label+u' '
                    elif s1.strip():
                        s += s1.strip() + u'/B-' + label + u' '
                    else:
                        pass
                else:
                    if ' ' in sent.strip():
                        s+=u'/O '.join(sent.split())+u'/O '
                    elif sent.strip():
                        s+=sent.strip()+u'/O'+u' '
                    else:
                        pass
        else:
            s+='/O '.join(line.strip().split())+'/O'

        return s



		
def add_color(line):
	num_buff=[]
	#print line
	if u'[@' not in line:
		pass
	else:
		tmp=line.split(u'[@')
		num=0
		start=0
		end=0
		for w in tmp:
			if u'*]' in w:
				start=num
				#print w
				end=num+len(u'[@')+w.index(u'*]')+2
				entity=w[w.index(u'#')+1:w.index(u'*]')]
				num_buff.append(['1.'+str(start),'1.'+str(end),entity])
				num+=len(u'[@')+len(w)
			else:
				num+=len(w)
	return num_buff

def cutthree(line):	
	line_new=[ w+u'-None' if u'/O' in w else w for w in line.split()]
	words=[]
	labels=[]
	wtypes=[]
	for w in line_new:
		ind1=w.index(u'/')  
		ind2=w.index(u'-')   
		words.append(w[:ind1])
		labels.append(w[ind1+1:ind1+2])
		wtypes.append(w[ind2+1:])
	return words,labels,wtypes
	
def likecrf(labels):
	'''根据BIO列表中的索引来合并词语列表'''
	start_l=0
	num=0
	buff=[]
	for i in range(len(labels)-1):
		start=num
		if labels[i]==u'B':
			if labels[i+1]!=u'I':
				buff.append([start,start+1]) #如果是只有一个B，则把起始位置记录在列表里输出
				num+=1
			else:
				start_l=num				
				num+=1
		if labels[i]==u'I':
			if labels[i+1]=='I':				
				num+=1				
			else:				
				num+=1				
				buff.append([start_l,start+1])			
		if labels[i]==u'O':			
			num+=1		
	return buff

	




#总控程序
def main():
    app=UI(Tk())
    app.master.title("命名实体人工标注工具")
    app.master.geometry("1300x650+10+10")
    app.mainloop()
    #root = Tk()
    #root.title("命名实体人工标注工具")
    #root.geometry("1300x700+200+200")
    #app=UI(root)
    #mainloop()
if __name__=='__main__':
    main()



