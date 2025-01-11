# NOTE: open Firefox to any page (so that Firefox is running)
from datatool import datatool

dt = datatool()

dt.load_csv('simpledata.csv')
dt.print_data()


# A basic line graph. 'X' and 'Y' are the column headers.
dt.line_graph('X', 'Y')

dt.display()
