from pyq import q
from datetime import date

#googdata:([]dt:();high:();low:();open:();close:();volume:(),adj_close:())

q.insert('eurusddata', (date(2014, 09, 2), 1.316099, 1.312405, 1.313094, 1.313198, 0.0, 1.313198))
q.insert('eurusddata', (date(2014, 09, 3), 1.3155, 1.29242, 1.314924, 1.315097, 0.0, 1.315097))

q.eurusddata.show()
                High       Low      Open     Close     Volume  Adj Close
Date
2014-09-02  1.316099  1.312405  1.313094  1.313198        0.0   1.313198
2014-09-03  1.3155    1.29242   1.314924  1.315097        0.0   1.315097

# f:{[s]select from eurusddata where date=d}

x=q.f('2014-09-02')
print(x.show())

2014-09-02  1.316099  1.312405  1.313094  1.313198        0.0   1.313198
