from cms10.models import Contact, SSOffice

class MergeDataExtractorException(Exception):
    pass

class NonGetRequest(MergeDataExtractorException):
    pass

class UnknownRequestParameter(MergeDataExtractorException):
    pass

class MergeDataExtractor(object):
    """parameter: request
        lookup model data from request arg and for each nonempty field add to merge data dict
    """
    def __init__(self,request, obj_map = None):
        self.object_mapping = { 'contact': Contact,
                                'claimant':Contact,
                                'fo':SSOffice,
                                'dds': SSOffice,
                                'odar':SSOffice,
                                'ac':SSOffice,
                                'alj':SSOffice,
                                'token':None}   # added to avoid error
        if obj_map:
            self.object_mapping = obj_map
        self.request = request
        self.merge_data_dic = {}
        if self.request.method == 'GET':
            dic = self.create_merge_data_dic_from_args()
            self.merge_data_dic.update(dic)
        else:
            raise NonGetRequest

    def get_model_data_from_db(self, k, v):
        qry_result = None
        if not k in self.object_mapping:
            raise UnknownRequestParameter

        if k in  ['contact', 'claimant','alj']:
            qry_result = Contact.query.get(v)
        elif k in ['fo','dds','odar', 'ac']:
            qry_result = SSOffice.query.get(v)

        if qry_result is None:
                return None
        else:
            res = qry_result.as_json()
            return res

    def create_merge_data_dic_from_args(self):
        """extract args from request add to dictionary
            for each arg keyword paid retrieve the model data uses as merge...
        """
        ret_dic = {}
        args_dict = {}
        #  change request args to mutable dict and then remove 'token' from arguments since only was need for authentication
        args_dict = self.request.args.to_dict()
        args_dict.pop('token', None)
        if len(args_dict) == 0:
            return None
        for arg,val in args_dict.items():
            model_data_dic = self.get_model_data_from_db(arg,val )
            if model_data_dic is None:
                return None
            else:
                prefix = arg + '_'
                for k,v in model_data_dic.items():
                    if v:                               # only add to dic if value not empty
                        ret_dic[prefix+k] = v           #should this be converted to unicode??
        return ret_dic

    def get_merge_data_dic(self):
        return self.merge_data_dic



