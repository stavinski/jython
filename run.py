from java.lang import Runnable
from javax.swing import JFrame, JPanel, JTabbedPane, SwingUtilities, JLabel, SwingConstants, JTextArea
from uicomponents import TabComponent, TabComponentCloseListener, TabComponentTitleChangedListener, TabComponentEditableTabMixin,TabComponentCloseableMixin
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
        tab.tabbed_pane = self.tabbedpane
        tab.addTitleChangedListener(App.TitleChangedListener())
        tab.addCloseListener(self)
        tab.text = 'Test'
        
        tab2 = MyUberTabComponent()
        tab2.tabbed_pane = self.tabbedpane
        tab2.addTitleChangedListener(App.TitleChangedListener())
        tab2.addCloseListener(self)
        tab2.text = 'Test 2'

        tabPanel = JPanel(BorderLayout(), opaque=False)
        tabPanel.add(JLabel('''<html><body>
<div style="font-size: 16pt;text-align:center">
Here is a Label.
</div></body></html>''', SwingConstants.CENTER))

        tab2Panel = JPanel(BorderLayout())
        text_area = JTextArea(font=Font('monospace', Font.PLAIN, 14))
        tab2Panel.add(text_area)

        self.tabbedpane.addTab(None, tabPanel)
        self.tabbedpane.setTabComponentAt(0, tab)
        self.tabbedpane.addTab(None, tab2Panel)
        self.tabbedpane.setTabComponentAt(1, tab2)

        panel.add(self.tabbedpane)

        frame.pack()
        frame.size = 600,600
        frame.defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        frame.locationRelativeTo = None
        frame.setVisible(True)
    
    def tabClose(self, event):
        idx = self.tabbedpane.indexOfTabComponent(event.getSource())
        self.tabbedpane.remove(idx)

    class TitleChangedListener(TabComponentTitleChangedListener):

        def titleChanged(self, event):
            print(event.getTitle())


if __name__ == '__main__':
    app = App()
    SwingUtilities.invokeLater(app)
