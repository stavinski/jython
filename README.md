# Jython

Not much to say... basically a repo to store any jython code.

## UI Components

Components to help with creating UIs specifically for Burp Extensions which allow jython to be used.

Have created a basic `run.py` script so you can try out these components:

~~~sh
java -jar <jython>.jar run.py
~~~

### Tabs

#### Intro

Ever wanted a more custom tab like the ones used in Burp such as the Repeater tab that allow renaming and closing? Look no further I have created 2 mixin classes that support both of these:

* `TabComponentEditableTabMixin`
* `TabComponentCloseableMixin`

Both of these expect the base class to be a `TabComponent` which is basically a simple `JPanel` subclass and would also allow some common methods to be placed here.

#### Usage

Copy the `uicomponents.py` into the same location as your script, decide which features you want to add to your tab and import them:

~~~python
from uicomponents import TabComponent, TabComponentEditableTabMixin,TabComponentCloseableMixin 
~~~

Then you will want to create a class that uses `TabComponent` as the base class and mixes in the correct features:

~~~python
class MyUberTabComponent(TabComponentEditableTabMixin, TabComponentCloseableMixin, TabComponent):
    pass 
~~~

The features will be applied in the order they are mixed into the class left to right. You can then use this with a `JTabbedPane` the same way you would with a custom tab component:

~~~python
tabbedpane = JTabbedPane()
tab = MyUberTabComponent()
tab.setText('Test')
        
tabbedpane.addTab(None, JPanel())
tabbedpane.setTabComponentAt(0, tab)
~~~

#### Common Questions?

Q. How to actually remove the tab from the `JTabbedPane`?
A. In order to actually allow the client to choose if the tab should be should be removed from the tabs (like providing a confirmation dialog) the mixin does not make any calls to the containing `JTabbedPane` in fact it knows nothing about it, instead an event is raised that can be listened to you can then use the following code to remove the tab:

~~~python
# tab and tabbedpane previously declared and current class implements TabComponentCloseListener
self.tab.addCloseListener(self)

def tabClose(self, event):
    idx = self.tabbedpane.indexOfTabComponent(event.getSource())
    self.tabbedpane.remove(idx)
~~~

Q. Can I make any customisations to the provided feature components?
A. Yes of course this being (J/P)ython you have full access to the the instance attributes, for instance if you wanted the text in the `JTextField` to be styled differently, simply change it in the class you created:

~~~python
class MyUberTabComponentWithBigText(TabComponentEditableTabMixin, TabComponentCloseableMixin, TabComponent):

    def __init__(self):
        super(MyUberTabComponent, self).__init__()   
        self.text_field.font = Font(Font.DIALOG, Font.BOLD, 15) 
~~~

Simply make sure it is performed after the call to the mixins and be careful not to intefere with how they operate oherwise should be all good!
