class OktaError(Exception):

    def __init__(self, error):
        if error is None:
            error = {}

        super(OktaError, self).__init__(error.get('errorSummary'))

        self.error_causes = error.get('errorCauses')
        self.error_code = error.get('errorCode')
        self.error_id = error.get('errorId')
        self.error_link = error.get('errorLink')
        self.error_summary = error.get('errorSummary')
        self.status_code = error.get('status_code')
