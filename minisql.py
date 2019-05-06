from __future__ import division
import math
import sys

Where_error=[]
From_error=[]
found_attributes={}
found_attributes_order=[]
operators=['>','<','=','<=','>=']
f=open('metadata.txt','r')
p=f.read()
p=p.split('\r\n')
tables={}
i=0
while i<len(p):
	if p[i]=='<begin_table>':
		i+=1
		table_name=p[i]
		i+=1
		table_attributes=[]
		while p[i]!='<end_table>':
			table_attributes.append(p[i])
			i=i+1
		tables[table_name]=table_attributes
	i=i+1

#print tables
inp=sys.argv
inp=inp[1:][0]

fl=0
Select=[]
From=[]
Where=[]
i=0
inp=inp.split()

while i<len(inp):
	if i<len(inp) and inp[i].lower()=='select':
		i+=1
		while i<len(inp) and inp[i].lower()!='from':
			if inp[i]=='metadata.txt':
				fl=1
			Select.append(inp[i])
			i=i+1
	if i<len(inp) and inp[i].lower()=='from':
		i+=1
		while i<len(inp) and inp[i].lower()!='where':
			if inp[i]=='metadata.txt':
				fl=1
			From.append(inp[i])
			i=i+1
	if i<len(inp) and inp[i].lower()=='where':
		i=i+1
		while i<len(inp):
			if inp[i]=='metadata.txt':
				fl=1
			Where.append(inp[i])
			i=i+1
		if len(Where)==0:
			print 'invalid syntax'
			exit()
	i=i+1

if len(Select)==0 or len(From)==0:
	print 'invalid syntax'
	exit()
def commabreak(Select):	
	s=''
	for i in range(0,len(Select)):
		l=Select[i].split(',')
		for j in range(0,len(l)):
			s=s+l[j]+' '
	s=s[0:len(s)-1]
	Select=s.split()
	return Select

if fl==1:
	Select=[]
	Select.append('*')

Select=commabreak(Select)
From=commabreak(From)
Where=commabreak(Where)

# print Select,From,Where
for i in range(0,len(From)):
	if From[i] not in tables:
		From_error.append(From[i])

def getdata(filename):
	ans=[] 
	file=filename+'.csv'
	f=open(file,'r')
	data=f.read()
	data=data.split('\n')
	for j in range(0,len(data)):
		p=data[j].split(',')
		if p[0]!='':
			ans.append(p)
	return ans

def crossproduct(list1,list2):
	ans=[]
	for i in range(0,len(list1)):
		for j in range(0,len(list2)):
			ans.append(list1[i]+list2[j])
	return ans

def printdata(ans,flagx):
	final=[]
	for i in range(0,len(ans)):
		p=[]
		if flagx[i]==1:
			for j in range(0,len(ans[0])):
				p.append(ans[i][j])
		if len(p)>0:
			final.append(p)
	return final

def printheaders(Select):
	st=''
	for i in range(0,len(Select)):
		st=st+Select[i]+','
	print st[0:len(st)-1]
	return

def finalprint(ans):
	for i in range(0,len(ans)):
		s=''
		for j in range(0,len(ans[0])):
			s=s+ans[i][j]+','
		print s[0:len(s)-1]
	return
def getall(From):
	ans=getdata(From[0])
	# print ans
	for i in range(1,len(From)):
		data=getdata(From[i])
		ans=crossproduct(ans,data)
	return ans

def get_positions(l,att1,att2,table_names):
	first=-1
	second=-1
	for i in range(0,len(l)):
		if att1 == l[i] or att1 == table_names[i]:
			first=i
		if att2 == l[i] or att2 == table_names[i]:
			second=i
	list1=[]
	list1.append(first)
	list1.append(second)
	return list1

def checkvalidity(ans,i,first,att1):
	p=0
	r=0
	try :
		p=int(att1)
	except:
		if first>=0:
			try:
				p=int(ans[i][first])
			except:
				Where_error.append(att1)
				r=-1
		else:
			Where_error.append(att1)
			r=-1
	return [p,r]

def single_equal(l,table_names,ans,att1,att2,flag,st):
	list1=get_positions(l,att1,att2,table_names)
	first=list1[0]
	second=list1[1]

	p=-1
	q=-1
	for i in range(0,len(ans)):		
		[p,r]=checkvalidity(ans,i,first,att1)
		[q,r]=checkvalidity(ans,i,second,att2)
		if r==-1:
			break
		if st=='none' and p==q:
			flag[i]=1
		if st=='and':
			if flag[i]==1 and p==q:
				flag[i]=1
			else:
				flag[i]=0

	return flag

def single_lessthan(l,table_names,ans,att1,att2,flag,st):
	list1=get_positions(l,att1,att2,table_names)
	first=list1[0]
	second=list1[1]
	
	p=-1
	q=-1
	for i in range(0,len(ans)):
		[p,r]=checkvalidity(ans,i,first,att1)
		[q,r]=checkvalidity(ans,i,second,att2)
		if r==-1:
			break
		if st=='none' and p<q:
			flag[i]=1
		if st=='and':
			if flag[i]==1 and p<q:
				flag[i]=1
			else:
				flag[i]=0

	# print flag
	return flag

def single_lessthan_equal(l,table_names,ans,att1,att2,flag,st):
	list1=get_positions(l,att1,att2,table_names)
	first=list1[0]
	second=list1[1]

	p=-1
	q=-1
	for i in range(0,len(ans)):
		[p,r]=checkvalidity(ans,i,first,att1)
		[q,r]=checkvalidity(ans,i,second,att2)
		if r==-1:
			break
		if st=='none' and p<=q:
			flag[i]=1
		if st=='and':
			if flag[i]==1 and p<=q:
				flag[i]=1
			else:
				flag[i]=0

	return flag

def single_greaterthan(l,table_names,ans,att1,att2,flag,st):
	list1=get_positions(l,att1,att2,table_names)
	first=list1[0]
	second=list1[1]
	p=-1
	q=-1

	for i in range(0,len(ans)):
		[p,r]=checkvalidity(ans,i,first,att1)
		[q,r]=checkvalidity(ans,i,second,att2)
		if r==-1:
			break
		if st=='none' and p>q:
			flag[i]=1
		if st=='and':
			if flag[i]==1 and p>q:
				flag[i]=1
			else:
				flag[i]=0

	return flag

def single_greaterthan_equal(l,table_names,ans,att1,att2,flag,st):
	list1=get_positions(l,att1,att2,table_names)
	first=list1[0]
	second=list1[1]
	p=-1
	q=-1

	for i in range(0,len(ans)):
		[p,r]=checkvalidity(ans,i,first,att1)
		[q,r]=checkvalidity(ans,i,second,att2)
		if r==-1:
			break
		if st=='none' and p>=q:
			flag[i]=1
		if st=='and':
			if flag[i]==1 and p>=q:
				flag[i]=1
			else:
				flag[i]=0

	return flag

if len(From_error)==0:	
	l=[]
	table_names=[]
	for i in range(0,len(From)):
		l=l+tables[From[i]]
		for j in range(0,len(tables[From[i]])):
			table_names.append(From[i]+'.'+tables[From[i]][j])
	found={}

	for i in range(0,len(l)):
		if l[i] not in found:
			found[l[i]]=1
		else:
			found[l[i]]+=1

	for i in range(0,len(l)):
		if found[l[i]]>1:
			l[i]=table_names[i]

	# print table_names
	# print l
	# print Where


	s=''
	i=0
	while i<len(Select):
		for j in range(0,len(Select[i])):		
			if Select[i][j]=='(':
				s=s+' ( '
			elif Select[i][j]==')':
				s=s+' ) '
			else:
				s=s+Select[i][j]
		s=s+' '
		i=i+1

	maxi=0
	mini=0
	sumi=0
	avgi=0
	distinct=0

	Select=s.split()
	if Select[0].lower()=='max':
		Select=[Select[2]]
		maxi=1
	elif Select[0].lower()=='min':
		Select=[Select[2]]
		mini=1
	elif Select[0].lower()=='avg':
		Select=[Select[2]]
		avgi=1
	elif Select[0].lower()=='sum':
		Select=[Select[2]]
		sumi=1
	elif Select[0].lower()=='distinct':
		distinct=1

	for i in range(0,len(Select)):
		if i+2<len(Select) and Select[i]=='(' and Select[i+2]!=')':
			print 'invalid syntax'
			exit()
		elif i>=2 and Select[i]==')'and Select[i-2]!='(':
			print 'invalid syntax'
			exit()
		elif Select[i]==')' and i<2:
			print 'invalid syntax'
			exit()
		elif Select[i]=='(' and i+2>=len(Select):
			print 'invalid syntax'
			exit()

	if distinct==1:
		s=''
		for i in range(0,len(Select)):
			s=s+Select[i]+' '
		Select=s.split()

		s=''
		for i in range(0,len(Select)):
			if i>=2 and i+1<len(Select) and Select[i-1]=='(' and Select[i+1]==')' and Select[i-2].lower()=='distinct':
				s=s+Select[i]+' '
			elif i>=2 and i+1<len(Select) and Select[i-1]=='(' and Select[i+1]==')' and Select[i-2].lower()!='distinct':
			# else:
				print 'invalid syntax'
				exit()

		s=s.split()
		Select=s
	if len(Select)==0:
		print 'invalid syntax'
		exit()	

	if Select[0]=='*':
		# print table_names
		Select=table_names+Select[1:]
		# ans=getall(From)
		# print ans
		# print_output(ans)
	positions=[]
	for i in range(0,len(Select)):
		positions.append(-1)

	ans=getall(From)
	for i in range(0,len(Select)):
		if Select[i] in l:
			ind=l.index(Select[i])
			positions[i]=ind
		if Select[i] in table_names:
			ind=table_names.index(Select[i])
			positions[i]=ind

	s=''
	for i in range(0,len(Where)):
		s=s+Where[i]+' '
	s=s[0:len(s)-1]

	i=0
	while i<len(s):
		if s[i]=='=':
			s=s[0:i]+' '+'='+' '+s[i+1:]
			i=i+2
		elif s[i]=='>':
			if s[i+1]=='=':
				s=s[0:i]+' '+'>='+' '+s[i+2:]
			else:
				s=s[0:i]+' '+'>'+' '+s[i+1:]
			i=i+2
		elif s[i]=='<':
			if s[i+1]=='=':
				s=s[0:i]+' '+'<='+' '+s[i+2:]
			else:
				s=s[0:i]+' '+'<'+' '+s[i+1:]
			i=i+2
		i=i+1

	Where=s.split()
	CheckWhere=[]
	# print Where

	invalid=0
	if len(Where)>0:
		if len(Where)!=3 and len(Where)!=7:
			invalid=1
		else:
			if Where[0] in operators or Where[1] not in operators or Where[2] in operators:
				invalid=1
			if len(Where)==7:
				if Where[3].lower()!='and'and Where[3].lower()!='or':
					invalid=1
				else:
					if Where[4] in operators or Where[5] not in operators or Where[6] in operators:
						invalid=1
		if invalid==1:
			print 'invalid syntax'
			exit()
	# print Select
	flagx=[]
	if len(Where)==0:
		for i in range(0,len(ans)):
			flagx.append(1)
	else:
		for i in range(0,len(ans)):
			flagx.append(0)

	d1=-1
	d2=-1
	d3=-1
	d4=-1
	if len(Where)>0:
		if Where[1]=='=':
			d1=Where[0]
			d2=Where[2]
			flagx=single_equal(l,table_names,ans,Where[0],Where[2],flagx,'none')
		if Where[1]=='<':
			flagx=single_lessthan(l,table_names,ans,Where[0],Where[2],flagx,'none')

		if Where[1]=='<=':
			flagx=single_lessthan_equal(l,table_names,ans,Where[0],Where[2],flagx,'none')

		if Where[1]=='>':
			flagx=single_greaterthan(l,table_names,ans,Where[0],Where[2],flagx,'none')

		if Where[1]=='>=':
			flagx=single_greaterthan_equal(l,table_names,ans,Where[0],Where[2],flagx,'none')

	# print flagx


	if len(Where)>3:
	 	if Where[3].lower()=='and':
			if Where[5]=='=':
				d3=Where[4]
				d4=Where[6]
				flagx=single_equal(l,table_names,ans,Where[4],Where[6],flagx,'and')

			if Where[5]=='<':
				flagx=single_lessthan(l,table_names,ans,Where[4],Where[6],flagx,'and')

			if Where[5]=='<=':
				flagx=single_lessthan_equal(l,table_names,ans,Where[4],Where[6],flagx,'and')

			if Where[5]=='>':
				flagx=single_greaterthan(l,table_names,ans,Where[4],Where[6],flagx,'and')

			if Where[5]=='>=':
				flagx=single_greaterthan_equal(l,table_names,ans,Where[4],Where[6],flagx,'and')

		elif Where[3].lower()=='or':
			if Where[5]=='=':
				d3=Where[4]
				d4=Where[6]
				flagx=single_equal(l,table_names,ans,Where[4],Where[6],flagx,'none')

			if Where[5]=='<':
				flagx=single_lessthan(l,table_names,ans,Where[4],Where[6],flagx,'none')

			if Where[5]=='<=':
				flagx=single_lessthan_equal(l,table_names,ans,Where[4],Where[6],flagx,'none')

			if Where[5]=='>':
				flagx=single_greaterthan(l,table_names,ans,Where[4],Where[6],flagx,'none')

			if Where[5]=='>=':
				flagx=single_greaterthan_equal(l,table_names,ans,Where[4],Where[6],flagx,'none')
			

	#print positions
	# print flagx
	# print flagy
	ans=printdata(ans,flagx)

	new=[[0 for x in range(len(Select))] for y in range(len(ans))]

	for i in range(0,len(positions)):
		for j in range(0,len(ans)):
			new[j][i]=ans[j][positions[i]]

	i1=-1
	i2=-1
	i3=-1
	i4=-1

	if d1!=-1 and d2!=-1:
		if d1 in Select:
			i1=Select.index(d1)
		if d2 in Select:
			i2=Select.index(d2)
	if d3!=-1 and d4!=-1:
		if d3 in Select:
			i3=Select.index(d3)
		if d4 in Select:
			i4=Select.index(d4)

	if i3==i1 and i4==i2:
		i3=-1
		i4=-1
	# print Select
	# print i1,i2,i3,i4

	# print new
	if maxi==0 and mini==0 and avgi==0 and sumi==0 and distinct==0:
		f=0
		s=''
		for i in range(0,len(positions)):
			if positions[i]==-1:
				f=1
				s=s+Select[i]+','
		if f==1:
			print s,'not specified clearly in select'
			s=''
		if len(Where_error)>0:
			for i in range(0,len(Where_error)):
				s=s+Where_error[i]+','
			print s,'not specified clearly in where'
		if f==0 and len(Where_error)==0:
			if i1!=-1 and i2!=-1 and i3!=-1 and i4!=-1:
				s=[]
				for i in range(0,len(Select)):
					if i!=i2 and i!=i4:
						s.append(Select[i])
				# print s
				printheaders(s)

				final=[[0 for x in range(len(new[0])-2)] for y in range(len(new))] 
				col=0
				for j in range(0,len(new[0])):
					if j!=i2 and j!=i4:
						for i in range(0,len(new)):
							final[i][col]=new[i][j]
						col+=1
				finalprint(final)
			elif i1!=-1 and i2!=-1:
				s=[]
				for i in range(0,len(Select)):
					if i!=i2:
						s.append(Select[i])
				# print s
				printheaders(s)
				final=[[0 for x in range(len(new[0])-1)] for y in range(len(new))] 
				col=0
				for j in range(0,len(new[0])):
					if j!=i2:
						for i in range(0,len(new)):
							final[i][col]=new[i][j]
						col+=1
				finalprint(final)
			else:
				# print Select
				printheaders(Select)
				finalprint(new)
	else:
		if maxi==1:
			print 'max(',Select[0],')'
			maxi=int(new[0][0])
			for i in range(1,len(new)):
				maxi=max(maxi,int(new[i][0]))
			print maxi
		elif mini==1:
			print 'min(',Select[0],')'
			mini=int(new[0][0])
			for i in range(1,len(new)):
				mini=min(mini,int(new[i][0]))
			print mini
		elif sumi==1:
			print 'sum(',Select[0],')'
			sumi=int(new[0][0])
			for i in range(1,len(new)):
				sumi+=int(new[i][0])
			print sumi
		elif avgi==1:
			print 'avg(',Select[0],')'
			sumi=int(new[0][0])
			for i in range(1,len(new)):
				sumi+=int(new[i][0])
			avgi=sumi/len(new)
			print avgi
		elif distinct==1:
			# print Select
			printheaders(Select)
			distincts={}
			for i in range(0,len(new)):
				s=''
				for j in range(0,len(new[0])):
					s=s+new[i][j]+' '
				s=s[0:len(s)-1]
				if s not in distincts:
					print new[i]
					distincts[s]=1
else:
	s=''
	for i in range(0,len(From_error)):
		s=s+From_error[i]+' '
	print s,'not found'