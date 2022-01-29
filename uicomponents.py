from java.util import EventObject, EventListener
from javax.swing import JButton, JComponent, JPanel,JLabel, AbstractAction, JTextField, SwingUtilities
from javax.swing.event import EventListenerList
from java.awt.event import MouseAdapter, FocusListener, ActionListener, KeyEvent

class TabComponent(JPanel):    

    def __init__(self):
        self.opaque = False

    def addTitle(self, title):
        label = JLabel(title)
        self.add(label)


class TabComponentClosedEvent(EventObject):

    def __init__(self, source):
        # super(TabComponentClosedEvent, self).__init__(source) not sure why but this does not work :-/
        EventObject.__init__(self, source)

class TabComponentCloseListener(EventListener):
    def tabClose(event):
        pass

class TabComponentCloseableMixin(object):
    
    def __init__(self):
        self.listeners = EventListenerList()
        close_button = JButton(actionPerformed=self._clicked)
        close_button.setText(unichr(0x00d7))  # multiplication sign
        close_button.border = None
        close_button.contentAreaFilled = False
        self.add(close_button)
        super(TabComponentCloseableMixin, self).__init__()
        
    def addCloseListener(self, listener):
        self.listeners.add(TabComponentCloseListener, listener)

    def removeCloseListener(self, listener):
        self.listeners.remove(TabComponentCloseListener, listener)

    def _clicked(self, event):   
        event = TabComponentClosedEvent(self)
        for listener in self.listeners.getListeners(TabComponentCloseListener):
            listener.tabClose(event)

class TabComponentEditableTabMixin(object):
    
    def __init__(self):
        self.isEditing = False
        self.event_listener = TabComponentEditableTabMixin.EventListener(self)
        self.text_field = TabTextField()
        self.text_field.actionPerformed = self.submitted
        self.text_field.keyPressed = self.keyPressed
        self.text_field.addMouseListener(self.event_listener)
        self.text_field.addFocusListener(self.event_listener)
        self.addMouseListener(self.event_listener)
        self.addFocusListener(self.event_listener)
        self.add(self.text_field)
        super(TabComponentEditableTabMixin, self).__init__()
    
    def setText(self, text):
        self.text_field.text = text

    def setEditing(self, state):
        self.isEditing = state
        if self.isEditing:
            self._text = self.text_field.text  # save text in case need to revert
            self.text_field.enableEditing()
        else:
            self.text_field.disableEditing()

    def mouseClicked(self, event):
        if SwingUtilities.isLeftMouseButton(event) and event.clickCount == 2:
            self.setEditing(not self.isEditing)

    def keyPressed(self, event):
        if event.keyCode == KeyEvent.VK_ESCAPE:
            self.setText(self._text)  # set the text back
            self.setEditing(False)

    def submitted(self,event):
        self.setEditing(False)

    def focusLost(self, event):
        self.setEditing(False)

    class EventListener(MouseAdapter, FocusListener):
        
        def __init__(self, parent):
            self.parent = parent

        def mouseClicked(self, event):
            self.parent.mouseClicked(event)

        def focusGained(self, event):  # only required as multiple inheritance is not allowed on java classes
            pass

        def focusLost(self, event):
            self.parent.focusLost(event)


class TabTextField(JTextField):

    def __init__(self):
        JTextField.__init__(self)
        self.editable = False
        self.border = None    
        self.opaque = False
    
    def enableEditing(self):
        self.editable = True
        self.opaque = True
        self.caret.visible = True  # have to micro manage the caret
    
    def disableEditing(self):
        self.editable = False
        self.opaque = False
        self.caret.visible = False # have to micro manage the caret

    # required to allow tab to grow while editing
    def isValidateRoot(self):
        return False