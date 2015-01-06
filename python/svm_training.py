#!/usr/bin/python

## @svm_training.py
#  This file properly escapes POST data received from 'php/logic_loader.php',
#      parses the data, and sends respective portions of the POST data to
#      'python/data_creator.py'. data_creator.py is responsible for saving
#      the SVM dataset into the mySQL database.
#
#  Note: This script is executed from 'logic_loader.php' using the 'exec( ... )'
#        method. To return data to php, use a simple 'print' statement. For
#        example the following will return the arguments passed to this script:
#
#            print sys.argv[1]
#
#        Then, in php, we can capture this data by:
#
#            $output = exec("$command $parameters");
#            $arr_result = array('result' => $output);
#            $json = array_merge($json, $arr_result);
#
#        Which will allow us to return it via ajax, as follows:
#
#            print json_encode($json);
#
#        Note: we can only call `print json_encode($json)` once. The receiving
#              receiving javascript can interpret the data as follows:
#
#            console.log( data.result );
#
#  @import sys, provides various functions, and variables that can be used to
#      manipulate different parts of the Python runtime environment (i.e. argv).
#
#  Note: the term 'dataset' used throughout various comments in this file,
#        synonymously implies the user supplied 'file upload(s)', and XML url
#        references.
import sys, json
from data_creator import Training
from data_validator import Validator
from svm_json import JSON

if len(sys.argv) > 1:
  # local variables
  response_dataset_validation = []

  # validate SVM settings
  validator = Validator( sys.argv[1], 'training' )
  validator.data_validation()

  # validate dataset, and store dataset
  svm_entity = {'title': json.loads(sys.argv[1])['data']['settings'].get('svm_title', None), 'uid': 1}
  db_save    = Training( svm_entity, 'save_entity' )
  id_entity  = db_save.db_save_training()

  if ( json.loads(sys.argv[1])['data']['dataset'].get('file_upload', None) ):
    # validate MIME type for each dataset
    response_mime_validation = validator.file_upload_validation( sys.argv[1] )
    if ( response_mime_validation['json_data'] is False ): sys.exit()

    # convert each dataset as json, validate, and store in database
    else:
      json_dataset = {}
      svm_property = sys.argv[1]

      for val in response_mime_validation['json_data']['file_upload']:
        # csv to json
        if val['type'] in ('text/plain', 'text/csv'):
          try:
            json_dataset = {'id_entity': id_entity, 'svm_dataset': json.loads(JSON( val['filedata']['file_temp'][0]).csv_to_json())}
            json_validated = Validator( json_dataset )
            response_dataset_validation.append(json_validated.dataset_validation())

            db_save = Training( json_dataset, 'save_value' )
            db_save.db_save_training()
          except Exception as e:
            print e
            sys.exit()

        # xml to json
        elif val['type'] in ('application/xml', 'text/xml' ):
          try:
            json_dataset = {'id_entity': id_entity, 'svm_dataset': json.loads(JSON( val['filedata']['file_temp'][0]).xml_to_json())}
            json_validated = Validator( json_dataset )
            response_dataset_validation.append(json_validated.dataset_validation())

            db_save = Training( json_dataset, 'save_value' )
            db_save.db_save_training()
          except Exception as e:
            print e
            sys.exit()

else:
  msg = 'Please provide a training dataset in json format'
  print json.dumps({'error':msg}, separators=(',', ': '))
  sys.exit()
