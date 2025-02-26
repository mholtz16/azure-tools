import os
import pyodbc, struct
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# get blobs for a specific user in tscfeedback
def get_conn():
    connection_string= 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:tscfeedback-live.database.windows.net,1433;Database=tscfeedback-live;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

def get_blobs_by_tscid(tscid,conn):
    query = f'select u.UserId,ExternalId AS TSCID,UserRoleId,RoleId,r.ReviewId,MasterReviewId,Title,Description,MediaSource from feedback.[User] u right join feedback.ReviewUserRole rur on u.UserId = rur.UserId left join feedback.Review r on r.ReviewId = rur.ReviewId where RoleId = 1 and IsConversation = \'false\' and r.IsDeleted = \'false\' and r.ReviewExternalId = r.MasterReviewId  and u.ExternalId = \'{tscid}\';'
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

conn = get_conn()
blobs = get_blobs_by_tscid('aaac315d-56d6-4115-bf32-fbdff5879b83',conn)

for blob in blobs:
    print(f'name: {blob[6]} source: {blob[8]}')







tscid = 'aaac315d-56d6-4115-bf32-fbdff5879b83'
