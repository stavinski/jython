from java.lang import Runnable
from javax.swing import JFrame, JPanel, JTabbedPane, SwingUtilities
from uicomponents import TabComponent, TabComponentCloseListener, TabComponentEditableTabMixin,TabComponentCloseableMixin
from java.awt import BorderLayout, Font

class MyUberTabComponent(TabComponentEditableTabMixin, TabComponentCloseableMixin, TabComponent):

    def __init__(self):
        super(MyUberTabComponent, self).__init__()   
        self.text_field.font = Font(Font.DIALOG, Font.BOLD, 15) 


class App(Runnable, TabComponentCloseListener):

    def __init__(self):
        self.tabbedpane = JTabbedPane()

    def run(self):
        panel = JPanel(BorderLayout())
        frame = JFrame('Jython Test')
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        frame.add(panel)

        tab = MyUberTabComponent()
        tab.addCloseListener(self)
        tab.setText('Test')
        
        self.tabbedpane.addTab(None, JPanel())
        self.tabbedpane.setTabComponentAt(0, tab)

        panel.add(self.tabbedpane)

        frame.pack()
        frame.size = 600,600
        frame.defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        frame.locationRelativeTo = None
        frame.setVisible(True)
    
    def tabClose(self, event):
        idx = self.tabbedpane.indexOfTabComponent(event.getSource())
        self.tabbedpane.remove(idx)
    
if __name__ == '__main__':
    app = App()
    SwingUtilities.invokeLater(app)
