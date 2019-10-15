import wx 
import API
class windowClass(wx.Frame):

  def __init__(self, parent, title):
    super(windowClass, self).__init__(parent, title=title)
    self.panel = MyPanel(self)

class MyPanel(wx.Panel):
    def __init__(self,parent):
      super(MyPanel,self).__init__(parent)
      self.label = wx.StaticText(self, label = 'Select Locations', pos =(50,30))
      locations=['Holroyd', 'Castle Hill', 'Energylab D9', 'Energylab D7']
      self.combobox = wx.ComboBox(self, choices = locations, pos =(50,50))
      
      self.label2 = wx.StaticText(self, label='', pos = (50,80))
      
      self.button = wx.Button(self, label = 'Generate CSV file', pos = (130,130))

      self.Bind(wx.EVT_COMBOBOX, self.onCombo)
      self.button.Bind(wx.EVT_BUTTON, self.onGenerateCSVFile)

    def onCombo(self, event):
      comboValue = self.combobox.GetValue()
      self.label2.SetLabel('You have selected ' + comboValue)
      

    def onGenerateCSVFile(self, event):
      self.API.main()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = windowClass(parent=None, title='Wattwatcher CSV Generator')
        self.frame.Show()
        return True


app = MyApp()
app.MainLoop()


   
