"""OHLC data feed."""
import cgitb
import psycopg2

# set the appropriate credentials
conn = psycopg2.connect(dbname="emporos", user="postgres", password="iT@9767398")
cursor = conn.cursor()

SQL = '''SELECT  
    dt,high,low,open,close,volume, adj_close
FROM "EURUSD"  
WHERE dt BETWEEN '2019-11-08' AND '2019-11-09'  
ORDER BY dt  
LIMIT 100;'''


def query_ticks(date_from=None, date_to=None, period=None, limit=None):
    """Dummy arguments for now.  Return OHLC result set."""
    cursor.execute(SQL)
    ohlc_result_set = cursor.fetchall()

    return ohlc_result_set


def format_as_csv(ohlc_data, header=False):
    """Dummy header argument.  Return CSV data."""
    csv_data = 'dt,o,h,l,c,vol\n'

    for row in ohlc_data:
        csv_data += ('%s, %s, %s, %s, %s, %s\n' %
                     (row[0], row[1], row[2], row[3], row[4], row[5] + row[6]))

    return csv_data

if __name__ == '__main__':
    cgitb.enable()

    ohlc_result_set = query_ticks()
    csv_data = format_as_csv(ohlc_result_set)

    print('Content-Type: text/plain; charset=utf-8\n')
    print(csv_data)

    cursor.close()
