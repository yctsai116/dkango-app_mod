from django import forms


class OperatorInfo(forms.Form):
    senderCode = forms.CharField(max_length=9,
                                 widget=forms.TextInput(attrs={'class': "form-control", 'id': "senderCode"}))
    operatorCode = forms.CharField(label='operator code', max_length=10,
                                   widget=forms.TextInput(attrs={'class': "form-control", 'id': "operatorCode"}))
    unitCode = forms.CharField(label='unit code', max_length=10,
                               widget=forms.TextInput(attrs={'class': "form-control", 'id': "unitCode"}))
    identityType = forms.CharField(label='identify type', max_length=1,
                                   widget=forms.TextInput(attrs={'class': "form-control", 'id': "identifyType"}))
    cbCustId = forms.CharField(label='cb cust id', max_length=20,
                               widget=forms.TextInput(attrs={'class': "form-control", 'id': "cbCustId"}))
    ccCustId = forms.CharField(label='cc cust id', max_length=20,
                               widget=forms.TextInput(attrs={'class': "form-control", 'id': "ccCustId"}))
    custId = forms.CharField(label=' cust id', max_length=50,
                             widget=forms.TextInput(attrs={'class': "form-control", 'id': "custId"}))
    birthDt = forms.CharField(label='birth day',
                              widget=forms.TextInput(attrs={'class': "form-control", 'id': "birthDt", 'type': "date"}))
    custName = forms.CharField(label='cust name', max_length=200,
                               widget=forms.TextInput(attrs={'class': "form-control", 'id': "custName"}))

    msgNo = forms.CharField(label='cust name', max_length=200,
                            widget=forms.TextInput(attrs={'class': "form-control", 'id': "msgNo"}))

    txnCode = forms.CharField(label='cust name', max_length=200,
                              widget=forms.TextInput(attrs={'class': "form-control", 'id': "txnCode"}))

    txnTime = forms.CharField(label='cust name', max_length=200,
                              widget=forms.TextInput(attrs={'class': "form-control", 'id': "txnTime", "type": "date"}))

    receiveCode = forms.CharField(label='cust name', max_length=200,
                                  widget=forms.TextInput(attrs={'class': "form-control", 'id': "receiveCode"}))

    authorizerCode = forms.CharField(label='cust name', max_length=200,
                                     widget=forms.TextInput(attrs={'class': "form-control", 'id': "authorizerCode"}))


class RequestDetailsForm(forms.Form):
    api_content = forms.CharField(label='api_content', max_length=200,
                                     widget=forms.Textarea(attrs={'class': "form-control", 'id': "apiContent", "rows": 6}))
    notes = forms.CharField(label='api_content', max_length=200,
                                  widget=forms.Textarea(attrs={'class': "form-control", 'id': "notes", "rows": 6}))
