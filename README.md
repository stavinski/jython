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

Ever wanted a more custom tab like the ones used in BurpSuite such as the Repeater tab that allow renaming and closing? Look no further I have created 2 mixin classes that support both of these:

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
tab.tabbed_pane = tabbedpane
tab.text = 'Test'
        
tabbedpane.addTab(None, JPanel())
tabbedpane.setTabComponentAt(0, tab)
~~~

#### How it looks in BurpSuite

![Screenshot from BurpSuite](images/tab_in_burp.png)

#### Common Questions?

**Q.** How to actually remove the tab from the `JTabbedPane`?

**A.** In order to actually allow the client to choose if the tab should be should be removed from the tabs (like providing a confirmation dialog) the mixin does not make any calls to the containing `JTabbedPane`, instead an event is raised that can be listened to you can then use the following code to remove the tab:

~~~python
# tab and tabbedpane previously declared and current class implements TabComponentCloseListener
self.tab.addCloseListener(self)

def tabClose(self, event):
    idx = self.tabbedpane.indexOfTabComponent(event.getSource())
    self.tabbedpane.remove(idx)
~~~

**Q.** Can I make any customisations to the provided feature components?

**A.** Yes of course this being (J/P)ython you have full access to the the instance attributes, for instance if you wanted the text in the `JTextField` to be styled differently, simply change it in the class you created:

~~~python
class MyUberTabComponentWithBigText(TabComponentEditableTabMixin, TabComponentCloseableMixin, TabComponent):

    def __init__(self):
        super(MyUberTabComponent, self).__init__()   
        self.text_field.font = Font(Font.DIALOG, Font.BOLD, 15) 
~~~

Simply make sure it is performed after the super `__init__` call to the mixins and be careful not to intefere with how they operate otherwise should be all good!

#### TODO

* ~~Event fired when title changed...assume that the client wants this persisted somewhere~~
* ~~Colour change when hover over close button~~
* Offer an alternative to the Java OO based eventing i.e. allow a simple callback function to be provided


### BurpUI

#### Intro

The built-in editor provided by Burp Suite via the `callbacks.createTextEditor()` method is pretty awesome out of the box with support for line numbering, searching, copy/paste and key bindings already being provided. 

The only issue is that the API provided by the `ITextEditor` is a bit limited for instance being able to listen for events on document changes is not provided. When trying to add support for text editing this left 2 options either build it from scratch using some of the other text editor code available or harness the power of the built-in one but somehow hook into any extra functionality required, I started with option 1 but quickly changed my mind. In order to help I with this I have created the `BurpUI` class that contains a helper method to obtain the main `JTextArea` used by the component.

I may also look to extend out for other things such as being able to place button next to the search panel (see the clear button on the Burp Suite extensions output frame).

#### Usage

Pretty straightforward simply import `BurpUI` grab an instance of the `ITextEditor` and pass into `get_textarea`:

~~~python
from uicomponents import BurpUI

editor = callbacks.createTextEditor()
text_area = BurpUI.get_textarea(editor)

# now hook into the document listener
text_area.document.addDocumentListener(self)
~~~

