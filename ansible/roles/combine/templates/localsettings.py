from django.conf import settings


# Deployment type
COMBINE_DEPLOYMENT = 'server'


# Combine Install Location
COMBINE_INSTALL_PATH = '/opt/combine'


# Combine Front-End
APP_HOST = '{{ip_address}}'


# Spark Cluster Information
SPARK_HOST = '{{spark_host}}'
SPARK_PORT = {{spark_port}}
SPARK_APPLICATION_ROOT_PORT = {{spark_application_root_port}} # if taken, will automatically increment +100 from here until open port is found


# Spark tuning
SPARK_MAX_WORKERS = {{spark_max_workers}}
JDBC_NUMPARTITIONS = {{jdbc_numpartitions}}
SPARK_REPARTITION = {{spark_repartition}}
MONGO_READ_PARTITION_SIZE_MB = {{mongo_read_partition_size_mb}}
TARGET_RECORDS_PER_PARTITION = 5000


# Apache Livy settings
'''
Combine uses Livy to issue spark statements.
Livy provides a stateless pattern for interacting with Spark, and by proxy, DPLA code.
'''
LIVY_HOST = '{{livy_host}}'
LIVY_PORT = {{livy_port}}
LIVY_DEFAULT_SESSION_CONFIG = {
    'kind':'pyspark',
    'jars':[
    	'file:///usr/share/java/mysql.jar'
    ],
    'files':[
    	'file://%s/core/spark/es.py' % COMBINE_INSTALL_PATH.rstrip('/'),
    	'file://%s/core/spark/jobs.py' % COMBINE_INSTALL_PATH.rstrip('/'),
    	'file://%s/core/spark/record_validation.py' % COMBINE_INSTALL_PATH.rstrip('/'),
    	'file://%s/core/spark/utils.py' % COMBINE_INSTALL_PATH.rstrip('/'),
    	'file://%s/core/spark/console.py' % COMBINE_INSTALL_PATH.rstrip('/'),
    	'file://%s/core/xml2kvp.py' % COMBINE_INSTALL_PATH.rstrip('/'),
    ],

    # Spark conf overrides
	'conf':{
		'spark.ui.port':SPARK_APPLICATION_ROOT_PORT
	},

    # Spark application overrides
		# commented out, will default to 2gb for driver and executor, and grab all available cpu/cores
		# uncommented, provides some limited configurations for tuning Spark application created by Livy

	# e.g. small(ish) server, 4gb RAM, 2 cpu/cores
	# 'driverMemory':'512m',
	# 'driverCores':1,
	# 'executorMemory':'512m',
	# 'executorCores':1,
	# 'numExecutors':1
}


# Storage for avro files and other binary files
'''
Make sure to note file:// or hdfs:// prefix
'''
BINARY_STORAGE = 'file:///home/combine/data/combine'
WRITE_AVRO = False


# ElasicSearch server
ES_HOST = '{{elasticsearch_host}}'
INDEX_TO_ES = True


# ElasticSearch analysis
CARDINALITY_PRECISION_THRESHOLD = 100
ONE_PER_DOC_OFFSET = 0.05


# Service Hub
SERVICE_HUB_PREFIX = 'foo--'


# OAI Server
OAI_RESPONSE_SIZE = 500
COMBINE_OAI_IDENTIFIER = 'oai:YOUR_OAI_PREFIX'
METADATA_PREFIXES = {
	'mods':{
			'schema':'http://www.loc.gov/standards/mods/v3/mods.xsd',
			'namespace':'http://www.loc.gov/mods/v3'
		},
	'oai_dc':{
			'schema':'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
			'namespace':'http://purl.org/dc/elements/1.1/'
		},
	'dc':{
			'schema':'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
			'namespace':'http://purl.org/dc/elements/1.1/'
		},
}


# Database configurations for use in Spark context
COMBINE_DATABASE = {
	'jdbc_url':'jdbc:mysql://%s:3306/combine' % APP_HOST,
	'user':settings.DATABASES['default']['USER'],
	'password':settings.DATABASES['default']['PASSWORD']
}

# DPLA API
DPLA_RECORD_MATCH_QUERY = {{dpla_record_match_query}}
DPLA_API_KEY = '{{dpla_api_key}}'


# AWS S3 Credentials
AWS_ACCESS_KEY_ID = '{{aws_access_key_id}}'
AWS_SECRET_ACCESS_KEY = '{{aws_secret_access_key}}'
DPLA_S3_BUCKET = '{{dpla_s3_bucket}}'


# Analysis Jobs Org and Record Group
'''
This dictionary provides the name of the Organization and Record Group that Analysis Jobs will be created under.
Because Analysis jobs are extremely similar to other workflow jobs, but do not lend themselves towards the established
Organization --> Record Group --> Job hierarchy, this ensures they are treated similarily to other jobs, but skip the
need for users to manually create these somewhat unique Organization and Record Group.
	- it is recommended to make these names quite unique, to avoid clashing with user created Orgs and Record Groups
	- the Organization and Record Group names defined in ANALYSIS_JOBS_HIERARCHY will NOT show up in any Org or Record
	Group views or other workflows
	- it is quite normal, and perhaps even encouraged, to leave these as the defaults provided
'''
ANALYSIS_JOBS_HIERARCHY = {
	'organization':'AnalysisOrganizationf8ed4bfcefc4dbf87b588a5de9b7cc95', # suffix is md5 hash of 'AnalysisOrganization'
	'record_group':'AnalysisRecordGroupf660bb4826bea8b63fd773d27d687cfd' # suffix is md5 hash of 'AnalysisRecordGroup'
}

# Celery Configurations
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


# StateIO Configurations
'''
Configurations used for exporting/importing "states" in Combine, including Organizations, Record Groups,
Jobs, Validation Scenarios, Transformation Scenarios, etc.  These can be large in size, and potentially helpful
to preserve, so /tmp is not ideal here.
'''
STATEIO_EXPORT_DIR = '/home/combine/data/combine/stateio/exports'
STATEIO_IMPORT_DIR = '/home/combine/data/combine/stateio/imports'


# Mongo server
MONGO_HOST = '127.0.0.1'
