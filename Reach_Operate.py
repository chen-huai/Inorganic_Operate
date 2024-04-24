import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import chicon  # 引用图标
from Reach_Operate_Ui import *
from TableView_Ui import *

class MyMainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MyMainWindow, self).__init__(parent)
		self.setupUi(self)

		self.actionExport.triggered.connect(self.exportConfig)
		self.actionImport.triggered.connect(self.importConfig)
		self.actionExit.triggered.connect(MyMainWindow.close)
		self.pushButton_3.clicked.connect(self.searchReachMessage)
		# self.actionImport.triggered.connect(self.lineEdit.clear)
		# self.actionHelp.triggered.connect(self.lineEdit.clear)
		self.actionAuthor.triggered.connect(self.showAuthorMessage)
		self.pushButton_2.clicked.connect(self.getReachMessage)
		self.pushButton_1.clicked.connect(self.clearCon)
		# self.pushButton_1.clicked.connect(self.comboBox_4.clear)
		self.pushButton_1.clicked.connect(self.lineEdit_1.clear)


	def getConfig(self):
		# 初始化，获取或生成配置文件
		global configFileUrl
		global desktopUrl
		global now
		global last_time
		global today
		# getReachMessage
		global reachLimsNo
		global reachEnglish
		global reachChinese
		global reachCas
		global reachPurpose
		now = int(time.strftime('%Y'))
		last_time = now - 1
		today = time.strftime('%Y%m%d')
		desktopUrl = os.path.join(os.path.expanduser("~"), 'Desktop')
		configFileUrl = '%s/config' % desktopUrl
		configFile = os.path.exists('%s/config_reach.txt' % configFileUrl)
		# print(desktopUrl,configFileUrl,configFile)
		if not configFile:  # 判断是否存在文件夹如果不存在则创建为文件夹
			reply = QMessageBox.question(self, '信息', '确认是否要创建配置文件', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if reply == QMessageBox.Yes:
				if not os.path.exists(configFileUrl):
					os.makedirs(configFileUrl)
				MyMainWindow.createConfigContent(self)
				MyMainWindow.getConfigContent(self)
				self.textBrowser.setText("创建并导入配置成功")
			else:
				exit()
		else:
			MyMainWindow.getConfigContent(self)

	def getConfigContent(self):
		# 获取配置文件内容
		f1 = open('%s/config_reach.txt' % configFileUrl, "r", encoding="utf-8")
		global configContent
		configContent = {}
		i = 0
		for line in f1:
			if line != '\n':
				lineContent = line.split('||||||')
				# print(lineContent)
				configContent['%s' % lineContent[0]] = lineContent[1].split('\n')[0]
			i += 1
		# print(configContent)
		self.textBrowser.setText("配置获取成功")

	def createConfigContent(self):
		# 生成默认配置文件
		configContentName = ['选择ICP_Batch的输入路径和结果输出路径', 'Reach_Message_Import_URL','Reach_Message_File_Name']
		configContent = ['默认，可更改为自己需要的','Z:\\Inorganic\\Program\\1.Inorganic Operate\\1.New edition\\2.Model', 'REACH_SVHC_Candidate_List_Opinion.csv']
		f1 = open('%s/config_reach.txt' % configFileUrl, "w", encoding="utf-8")
		i = 0
		for i in range(len(configContentName)):
			f1.write(configContentName[i] + '||||||' + configContent[i] + '\n')
			i += 1
		self.textBrowser.setText("配置文件创建成功")
		QMessageBox.information(self, "提示信息",
								"默认配置文件已经创建好，\n如需修改请在用户桌面查找config文件夹中config_reach.txt，\n将相应的文件内容替换成用户需求即可，修改后记得重新导入配置文件。\n切记：中间‘||||||’六根，不能多也不能少！！！",
								QMessageBox.Yes)

	def exportConfig(self):
		# 重新导出默认配置文件
		reply = QMessageBox.question(self, '信息', '确认是否要创建默认配置文件', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			MyMainWindow.createConfigContent(self)
		else:
			QMessageBox.information(self, "提示信息", "没有创建默认配置文件，保留原有的配置文件", QMessageBox.Yes)

	def importConfig(self):
		# 重新导入配置文件
		reply = QMessageBox.question(self, '信息', '确认是否要导入配置文件', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			MyMainWindow.getConfigContent(self)
		else:
			QMessageBox.information(self, "提示信息", "没有重新导入配置文件，将按照原有的配置文件操作", QMessageBox.Yes)

	def showAuthorMessage(self):
		# 关于作者
		QMessageBox.about(self, "关于",
						  "人生苦短，码上行乐。\n\n\n        ----Frank Chen")

	def clearCon(self):
		self.spinBox_1.setValue(0)
		self.textBrowser.clear
		self.lineEdit_1.clear
		self.comboBox_4.setCurrentIndex(0)


	def getReachMessage(self):
		# 获取Reach信息
		global reachLimsNo
		global reachEnglish
		global reachChinese
		global reachCas
		global reachPurpose
		global reachMessage
		global searchReachMessage
		file = configContent['Reach_Message_Import_URL'] + '\\' + configContent['Reach_Message_File_Name']
		folder = os.path.exists(file)
		if not folder:
			QMessageBox.information(self, "无Reach信息模板",
									"没有Reach信息文件！！！\n请查看config_reach配置文件内容是否符合需求。\nReach_Message_Import_URL,Reach_Message_File_Name\nReach Message的文件路径、文件名称和CSV格式",
									QMessageBox.Yes)
		else:
			self.comboBox_4.clear()
			reachMessage = pd.read_csv(file)
			reachLimsNo = list(reachMessage['Lims No.'])
			reachEnglish = list(reachMessage['物质名称(英文)'])
			reachChinese = list(reachMessage['物质名称(中文)'])
			reachCas = list(reachMessage['CAS 号码'])
			reachPurpose = list(reachMessage['可能用途'])
			self.comboBox_4.addItem('')
			self.comboBox_4.addItems(sorted(set(reachCas)))
			self.textBrowser.setText("Reach信息获取成功")

	def searchReachMessage(self):
		# 搜索Reach信息提示
		try:
			reachLimsNo
		except NameError:
			reply = QMessageBox.question(self, '信息', '是否需要获取Reach信息文件', QMessageBox.Yes | QMessageBox.No,
										 QMessageBox.Yes)
			if reply == QMessageBox.Yes:
				MyMainWindow.getReachMessage(self)
				self.textBrowser.setText("请继续点击搜索按钮以搜索Reach信息")
			else:
				self.textBrowser.setText("请点击获取按钮以取得Reach信息")
		else:
			global project
			reachContent = self.lineEdit_1.text()
			reachNum = self.spinBox_1.text()
			casNum = self.comboBox_4.currentText()
			# 项目选择
			project = self.comboBox.currentText()
			# 只要物质信息的搜索
			if (reachContent == '') and (reachNum == '0') and (casNum == ''):
				global material, estimate
				# 物质选择
				material = self.comboBox_2.currentText()
				# 风险选择
				estimate = self.comboBox_3.currentText()
				# print(material, project, estimate)
				myTable.searchReachMessage()
			else:

				# if (reachContent != '') and (reachNum != '0') and (casNum != ''):
				#
				# 	if (reachContent  reachEnglish==reachLimsNo.index(reachNum) and (
				# 			casNum == reachCas[n]):
				# 		m = 'T'
				# else:
				# 	self.textBrowser.append(
				# 		"请确认查找Reach英文内容或者编号是否写对，\n当物质编号不为‘0’、物质内容和Cas No.不为空时，\n物质内容、编号和Cas No.要同时匹配才能查找Reach信息")
				# 	self.textBrowser.append('--------------------------')
				same = ''
				different = ''
				for n in range(len(reachLimsNo)):
					m = 'F'
					if (reachContent != '') and (reachNum != '0') and (casNum != ''):
						if (reachContent in reachEnglish[n]) and float(reachNum) == float(reachLimsNo[n]) and (
								casNum == reachCas[n]):
							m = 'T'
							num = n
							same = 'same'
						else:
							different = 'different'
					elif (reachContent != '') and (reachNum != '0'):
						if (reachContent in reachEnglish[n]) and float(reachNum) == float(reachLimsNo[n]):
							m = 'T'
							num = n
							same = 'same'
						else:
							different = 'different'

					elif (reachNum != '0') and (casNum != ''):
						if float(reachNum) == float(reachLimsNo[n]) and (casNum == reachCas[n]):
							m = 'T'
							num = n
							same = 'same'
						else:
							different = 'different'
					elif (reachContent in reachEnglish[n]) and (casNum != ''):
						if (reachContent in reachEnglish[n]) and (casNum == reachCas[n]):
							m = 'T'
							num = n
							same = 'same'
						else:
							different = 'different'

					elif reachContent != '':
							if (reachContent in reachEnglish[n]):
								m = 'T'
								num = n

					elif reachNum != '0':
						if float(reachNum) == float(reachLimsNo[n]):
							m = 'T'
							num = n
					elif casNum != '':
							if (casNum == reachCas[n]):
								m = 'T'
								num = n
					# print(m)
					if m == 'T':
						if self.checkBox.checkState():
							self.textBrowser.append("<table border='1'> <tr><th>目标</th> <th>内容</th></tr> <tr><td>Reach Lims No:</td><td>%s</td></tr> <tr><td>Reach 中文名:</td><td>%s</td></tr> <tr><td>Reach 英文名:</td><td>%s</td></tr> <tr><td>Reach CAS No:</td><td><font color='red'>%s</font></td></tr> <tr><td>Reach 物质作用:</td><td>%s</td></tr> </table>" % (reachLimsNo[num],reachChinese[num],reachEnglish[num],reachCas[num],reachPurpose[num]))
							self.textBrowser.append('--------------------------')
							app.processEvents()
						if self.checkBox_2.checkState():
							self.textBrowser.append("Reach Lims No:%s" % reachLimsNo[num])
							self.textBrowser.append("Reach 中文名:%s" % reachChinese[num])
							self.textBrowser.append("Reach 英文名:%s" % reachEnglish[num])
							self.textBrowser.append("Reach CAS No:%s\n" % reachCas[num])
							self.textBrowser.append("Reach 物质作用:\n%s" % reachPurpose[num])
							self.textBrowser.append('--------------------------')
							app.processEvents()
				if ((same == 'same') and (different == 'different')) or ((same == '') and (different == '')):
					pass
				else:
					self.textBrowser.append(
						"请确认查找Reach英文内容或者编号是否写对，\n当物质编号不为‘0’、物质内容和Cas No.不为空时，\n物质内容、编号和Cas No.要同时匹配才能查找Reach信息")
					self.textBrowser.append('--------------------------')


class MyTableWindow(QMainWindow, Ui_TableWindow):
	def __init__(self, parent=None):
		super(MyTableWindow, self).__init__(parent)
		self.setupUi(self)

		self.pushButton_4.clicked.connect(self.search)


	def search(self):
		global material, estimate,project
		# 物质选择
		material = self.comboBox.currentText()
		# 风险选择
		estimate = self.comboBox_3.currentText()
		# 项目选择
		project = self.comboBox_2.currentText()
		# print(material, project, estimate)
		myTable.searchReachMessage()

	def searchReachMessage(self):
		dropC = ['No.','列入日期','EC 号码','Possible Applications','*Remarks','Chemical Classification']
		maybeC = ['Natural textiles','Synthetic textiles','Leather','Metal','Plastic|polymers|foam','Wood','Paper','Ceramic','Glass','Dye|Pigment|Ink|Paint','Adhesives|Sealants','Battery','Electronic components']
		leaveC = ['Lims No.','CAS 号码','物质名称(英文)','物质名称(中文)','可能用途','Organic|Inorganic']
		csvHead = list(reachMessage.head())
		# 选择性显示
		if material != '':
			maybeC.remove(material)
		else:
			maybeC = []
		# if project != '':
		# 	maybeC.remove('Organic|Inorganic')
		# 	# reachMessage.loc[reachMessage['Organic|Inorganic'] == project]
		dropC += maybeC
		searchReachMessage = reachMessage.drop(dropC, axis=1)
		if project != '':
			# searchReachMessage要重新赋值才能保存成功
			searchReachMessage = searchReachMessage.loc[searchReachMessage['Organic|Inorganic'] == project]
		if material != '':
			if estimate != '':
				if estimate == 'Y':
					searchReachMessage = searchReachMessage.loc[(searchReachMessage[material] == 'Y')|(searchReachMessage[material] == 'Y*')]
				else:
					searchReachMessage = searchReachMessage.loc[(searchReachMessage[material] == 'N')|(searchReachMessage[material] == 'N*')]
		csvHead = list(searchReachMessage.head())
		# csvL = list(range(len(searchReachMessage.index)))
		# print(csvL)
		# res = pd.DataFrame(searchReachMessage,index=csvL,columns=csvHead)
		# searchReachMessage.reindex()
		res = pd.DataFrame(searchReachMessage,columns=csvHead)
		model = TableModel(res)
		self.tableView.setModel(model)
		self.tableView.setAlternatingRowColors(True)
		self.tableView.resizeRowsToContents()
		# self.tableView.setForegroundRole()setForeground(QBrush(QColor(255, 0, 0)));
		myTable.show()

# 将数据转换为table显示数据
class TableModel(QAbstractTableModel):
	def __init__(self, data):
		QAbstractTableModel.__init__(self)
		self._data = data

	def rowCount(self, parent=None):
		return self._data.shape[0]

	def columnCount(self, parent=None):
		return self._data.shape[1]

	# 显示数据
	def data(self, index, role=Qt.DisplayRole):
		if index.isValid():
			if role == Qt.DisplayRole:
				return str(self._data.iloc[index.row(), index.column()])
		return None

	# 显示行和列头
	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self._data.columns[col]
		elif orientation == Qt.Vertical and role == Qt.DisplayRole:
			return self._data.axes[0][col]
		return None


if __name__ == "__main__":
	import sys
	import os
	import time
	import pandas as pd
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
	app = QApplication(sys.argv)
	myWin = MyMainWindow()
	myTable = MyTableWindow()
	myWin.show()
	myWin.getConfig()
	sys.exit(app.exec_())