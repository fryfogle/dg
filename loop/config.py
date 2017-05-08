# -*- coding: utf-8 -*-

# Code snippet ad imports for email attachment with encodings. To be used in another file for attachmnet in emails

from django.template.context import Context
from django.template.loader import get_template
from django.core.mail.message import EmailMultiAlternatives
import mimetypes
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, EXOTEL_HELPLINE_NUMBER, MEDIA_ROOT

from django.core.mail.message import DEFAULT_ATTACHMENT_MIME_TYPE


class EmailMultiAlternativesWithEncoding(EmailMultiAlternatives):
    def _create_attachment(self, filename, content, mimetype=None):
        """
        Converts the filename, content, mimetype triple into a MIME attachment
        object. Use self.encoding when handling text attachments.
        """
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is None:
                mimetype = DEFAULT_ATTACHMENT_MIME_TYPE
        basetype, subtype = mimetype.split('/', 1)
        if basetype == 'text':
            encoding = self.encoding or settings.DEFAULT_CHARSET
            attachment = SafeMIMEText(smart_str(content,
                                                settings.DEFAULT_CHARSET), subtype, encoding)
        else:
            # Encode non-text attachments with base64.
            attachment = MIMEBase(basetype, subtype)
            attachment.set_payload(content)
            encoders.encode_base64(attachment)
        if filename:
            try:
                filename = filename.encode('ascii')
            except UnicodeEncodeError:
                filename = Header(filename, 'utf-8').encode()
            attachment.add_header('Content-Disposition', 'attachment',
                                  filename=filename)
        return attachment


#Extra variables required in other files
DEFAULT_COLUMN_WIDTH = 9

header_dict_for_loop_email_mobile_numbers = {
    'workbook_name': u'%s/loop/Incorrect Mobile Numbers_%s_%s to %s.xlsx',
    'worksheet_name': u'%s_गलत मोबाइल नंबर की लिस्ट_%s to %s',
    'column_properties': [{'column_width': 3.36,
                           'header': u'क्रम',
                           'col_seq': 'A:A',
                          },
                          {'column_width': 14.36,
                           'header': u'जमाकर्ता का\n नाम',
                           'col_seq': 'B:B',
                          },
                          {'column_width': 12,
                           'header': u'गांव का नाम',
                           'col_seq': 'C:C',
                          },
                          {'column_width': 6.36,
                           'header': u'किसान ID',
                           'col_seq': 'D:D',
                          },
                          {'column_width': 15,
                           'header': u'किसान का नाम',
                           'col_seq': 'E:E',
                          },
                          {'column_width': 8,
                           'header': u'सब्जी कितने\n दिन दी?',
                           'col_seq': 'F:F',
                          },
                          {'column_width': 10,
                           'header': u'मोबाइल नं',
                           'col_seq': 'G:G',
                          },
                          {'column_width': 11.27,
                           'header': u'कितने किसान\n में नंबर डला है?',
                           'col_seq': 'H:H',
                          }]
}

header_dict_for_farmer_outlier = {
    'workbook_name': u'%s/loop/Farmer Share Outliers_%s_%s to %s.xlsx',
    'worksheet_name': u'%s_फार्मर शेर आउटलाइयर्स की लिस्ट_%s to %s',
    'column_properties': [{'column_width': 9.09,
                            'header': 'Date',
                           'col_seq': 'A:A',
                           'data_type': 'Date'
                          },
                          {'column_width': 16.55,
                           'header': 'Aggregator',
                           'col_seq': 'B:B'
                          },
                          {'column_width': 14.64,
                              'header': 'Market',
                              'col_seq': 'C:C'
                          },
                          {'column_width': 7.55,
                              'header': 'Quantity',
                              'col_seq': 'D:D'
                          },
                          {'column_width': 8.55,
                              'header': 'Transport Cost',
                              'col_seq': 'E:E'
                          },
                          {'column_width': 6.09,
                              'header': 'Farmer Share',
                              'col_seq': 'F:F'
                          },
                          {'column_width': 6.0,
                              'header': 'Farmer Share Per KG',
                              'col_seq': 'G:G'
                          },
                          {'column_width': 12.0,
                              'header': 'Farmer Share/Transport Cost',
                              'col_seq': 'H:H'
                          }
    ]
}

header_dict_for_transport_outlier = {
    'workbook_name': u'%s/loop/Transport Share Outliers_%s_%s to %s.xlsx',
    'worksheet_name': u'%s_गाड़ी किराया आउटलाइयर्स की लिस्ट_%s to %s',
    'column_properties': [{'column_width': 10.64,
                            'header': 'Date',
                           'data_type': 'Date',
                           'col_seq': 'A:A'
                          },
                          {'column_width': 16,
                           'header': 'Aggregator',
                           'col_seq': 'B:B'
                          },
                          {'column_width': 14.55,
                              'header': 'Market',
                              'col_seq': 'C:C'
                          },
                          {'column_width': 7.55,
                              'header': 'Quantity',
                              'col_seq': 'D:D'
                          },
                          {'column_width': 12.73,
                              'header': 'Transport Cost',
                              'col_seq': 'E:E'
                          },
                          {'column_width': 7.45,
                              'header': 'Type',
                              'col_seq': 'F:F'
                          },
                          {'column_width': 11.2,
                              'header': 'Transport CPK',
                              'col_seq': 'G:G'
                          }
    ]
}

header_dict_for_farmer_details = [{'column_width': 3.64,
                           'label': 'क्रम',
                           'col_seq': 'A:A',
                          },
                          {'column_width': 9.82,
                           'label': 'तारीख',
                           'col_seq': 'B:B',
                          },
                          {'column_width': 11.55,
                           'label': 'मंडी का नाम',
                           'col_seq': 'C:C',
                          },
                          {'column_width': 15,
                           'label': 'किसान का नाम',
                           'col_seq': 'D:D',
                          },
                          {'column_width': 9.09,
                           'label': 'कुल वजन (कि.)',
                           'col_seq': 'E:E',
                          },
                          {'column_width': 7,
                           'label': 'राशि (रु)',
                           'col_seq': 'F:F',
                          },
                          {'column_width': 7.45,
                           'label': 'किसान का भाग (रु)',
                           'col_seq': 'G:G',
                          },
                          {'column_width': 8.36,
                           'label': 'कुल राशि (रु)',
                           'col_seq': 'H:H',
                          },
                          {'column_width': 5.91,
                           'label': '✓/ X',
                           'col_seq': 'I:I',
                          },
                          {'column_width': 16.55,
                           'label': 'टिप्पडी',
                           'col_seq': 'J:J',
                          }]


#
# query_for_farmer_transaction_all_aggregator = '''
#                                   SELECT
#                               t1.Agg,
#                               t1.date,
#                               t1.Mandi,
#                               t1.Farmer,
#                               Total_Quantity,
#                               Total_Amount,
#                               ts / tv * Total_Quantity fs,
#                               Total_Amount - (ts / tv * Total_Quantity) Net_Amount
#                           FROM
#                               (SELECT
#                                   lct.user_created_id Agg,
#                                       date,
#                                       lm.mandi_name Mandi,
#                                       lf.name Farmer,
#                                       SUM(quantity) Total_Quantity,
#                                       SUM(amount) Total_Amount
#                               FROM
#                                   loop_combinedtransaction lct
#                               JOIN loop_farmer lf ON lf.id = lct.farmer_id
#                               JOIN loop_mandi lm ON lct.mandi_id = lm.id
#                               GROUP BY Agg , date , Mandi , lct.farmer_id) t1
#                                   JOIN
#                               (SELECT
#                                   t2.user_ User_id,
#                                       t2.date Date_,
#                                       t2.mandi Mandi_,
#                                       t2.Total_Volume tv,
#                                       t3.Share_ ts
#                               FROM
#                                   (SELECT
#                                   lct.user_created_id user_,
#                                       date,
#                                       lm.mandi_name mandi,
#                                       SUM(quantity) Total_Volume
#                               FROM
#                                   loop_combinedtransaction lct
#                               JOIN loop_mandi lm ON lm.id = lct.mandi_id
#                               GROUP BY user_ , date , lct.mandi_id) t2
#                               JOIN (SELECT
#                                   dt.user_created_id,
#                                       date,
#                                       lm.mandi_name mandi_,
#                                       AVG(farmer_share) Share_
#                               FROM
#                                   loop_daytransportation dt
#                               JOIN loop_mandi lm ON dt.mandi_id = lm.id
#                               GROUP BY user_created_id , date , dt.mandi_id) t3 ON t2.user_ = t3.user_created_id
#                                   AND t2.date = t3.date
#                                   AND t2.mandi = t3.mandi_) t4 ON t1.Agg = t4.User_id
#                                   AND t1.date = t4.Date_
#                                   AND t1.Mandi = t4.Mandi_
#                           WHERE
#                               t1.date BETWEEN %s AND %s
#                         '''
#
#
# query_for_farmer_transaction_single_aggregator = '''
#                                   SELECT
#                                 t1.Agg,
#                                 t1.date,
#                                 t1.Mandi,
#                                 t1.Farmer,
#                                 Total_Quantity,
#                                 Total_Amount,
#                                 ts / tv * Total_Quantity fs,
#                                 Total_Amount - (ts / tv * Total_Quantity) Net_Amount
#                             FROM
#                                 (SELECT
#                                     lct.user_created_id Agg,
#                                         date,
#                                         lm.mandi_name Mandi,
#                                         lf.name Farmer,
#                                         SUM(quantity) Total_Quantity,
#                                         SUM(amount) Total_Amount
#                                 FROM
#                                     loop_combinedtransaction lct
#                                 JOIN loop_farmer lf ON lf.id = lct.farmer_id
#                                 JOIN loop_mandi lm ON lct.mandi_id = lm.id
#                                 GROUP BY Agg , date , Mandi , lct.farmer_id) t1
#                                     JOIN
#                                 (SELECT
#                                     t2.user_ User_id,
#                                         t2.date Date_,
#                                         t2.mandi Mandi_,
#                                         t2.Total_Volume tv,
#                                         t3.Share_ ts
#                                 FROM
#                                     (SELECT
#                                     lct.user_created_id user_,
#                                         date,
#                                         lm.mandi_name mandi,
#                                         SUM(quantity) Total_Volume
#                                 FROM
#                                     loop_combinedtransaction lct
#                                 JOIN loop_mandi lm ON lm.id = lct.mandi_id
#                                 GROUP BY user_ , date , lct.mandi_id) t2
#                                 JOIN (SELECT
#                                     dt.user_created_id,
#                                         date,
#                                         lm.mandi_name mandi_,
#                                         AVG(farmer_share) Share_
#                                 FROM
#                                     loop_daytransportation dt
#                                 JOIN loop_mandi lm ON dt.mandi_id = lm.id
#                                 GROUP BY user_created_id , date , dt.mandi_id) t3 ON t2.user_ = t3.user_created_id
#                                     AND t2.date = t3.date
#                                     AND t2.mandi = t3.mandi_) t4 ON t1.Agg = t4.User_id
#                                     AND t1.date = t4.Date_
#                                     AND t1.Mandi = t4.Mandi_
#                             WHERE
#                                 t1.date BETWEEN %s AND %s
#                                     AND t1.Agg = %s'''
#
#



RECIPIENTS = ['lokesh@digitalgreen.org', 'divish@digitalgreen.org']

RECIPIENTS_TEMP = ['amandeep@digitalgreen.org']


