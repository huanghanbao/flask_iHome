# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from ihome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8a216da8635e621f016369350f72067f'

# ���ʺ�Token
accountToken = '2ba652d60b2b40579e66a4646ed815b6'

# Ӧ��Id
appId = '8a216da8635e621f016369350fd10686'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


class CCP(object):
    def __init__(self):
        # ��ʼ��REST SDK
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    # ����ģ�����
    # @param to �ֻ�����
    # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
    # @param $tempId ģ��Id

    def send_template_sms(self, to, datas, tempId):
        result = self.rest.sendTemplateSMS(to, datas, tempId)

        if result.get('statusCode') == '000000':
            # ���ͳɹ�
            return 1
        else:
            # ����ʧ��
            return 0

# sendTemplateSMS(�ֻ�����,��������,ģ��Id)
if __name__ == '__main__':
    CCP().send_template_sms('13432979745', ['123456', 5], 1)

