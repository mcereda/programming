# Using Python with AWS

Refer [Boto3 documentation].

1. [TL;DR](#tldr)
1. [Clients](#clients)
1. [Resources](#resources)
1. [Sessions](#sessions)
1. [Error handling](#error-handling)
1. [Further readings](#further-readings)
   1. [Sources](#sources)

## TL;DR

_Clients_ and _Resources_ are different abstractions for service requests within the Boto3 SDK.<br/>
When making API calls to an AWS service with Boto3, one does so via a _Client_ or a _Resource_.

<details style="padding: 0 0 0 1em">
  <summary>Client</summary>

```py
import boto3

s3 = boto3.client('s3')
try:
    paginator = client.get_paginator('list_objects_v2')
    # the paginator returns a generator; should one run through it, it will be spent
    # => save the paginator's results to a flattened list
    iterator = paginator.paginate(Bucket=someBucket)
    objects = []
    for obj in iterator:
        objects.extend(obj['Contents'])
    print(f'found {len(objects)} objects')
except botocore.exceptions.ClientError as e:
    print(e.response['Error']['Message'])
```

</details>
<details style="padding: 0 0 1em 1em">
  <summary>Resource</summary>

```py
import boto3

s3 = boto3.resource('s3')
try:
    bucket = s3.Bucket('someBucket')
    print(f'found {len([obj for obj in buck.objects.all()])} objects')
except botocore.exceptions.ClientError as e:
    print(e.response['Error']['Message'])
```

</details>

_Sessions_ are fundamental to both Clients and Resources and how both get access to AWS credentials.

## Clients

Provide low-level access to AWS services by exposing the `botocore` client to the developer.

Typically map 1:1 with the related service's API and supports all operations for the called service.<br/>
Expose Python-fashioned method names (e.g. ListBuckets API => list_buckets method).

Typically yield primitive, non-marshalled AWS data.<br/>
E.g. DynamoDB attributes are dictionaries representing primitive DynamoDB values.

Limited to listing at most 1000 objects, requiring the developer to deal with result pagination in code.<br/>
Use a [paginator][paginators] or implement one's own loop.

Paginators return a generator.<br/>
Should one run through a generator, it will be spent. Save the paginator's results to a flattened list for reuse.

## Resources

Refer [Resources].

Provide high-level, object-oriented code.

Do **not** provide 100% API coverage of AWS services.

Use identifiers and attributes, has actions (operations on resources), and exposes sub-resources and collections of
AWS resources.

Typically yield marshalled data, **not** primitive AWS data.<br/>
E.g. DynamoDB attributes are native Python values representing primitive DynamoDB values.

Take care of result pagination.<br/>
The resulting collections of sub-resources are lazily-loaded.

Are **not** thread safe and should **not** be shared across threads or processes.<br/>
Create a new Resource for each thread or process instead.

Since January 2023 the AWS Python SDK team stopped adding new features to the resources interface in Boto3.<br/>
Newer service features can be accessed through the Client interface.<br/>
Refer [More info about resource deprecation?] for more information.

## Sessions

Refer [Sessions].

Stores configuration information (primarily credentials and selected AWS Region).<br/>
Initiates the connectivity to AWS services.

Leveraged by service Clients and Resources.<br/>
Boto3 creates a default session automatically when needed, using the default credential profile.<br/>
The default credentials profile uses the `~/.aws/credentials` file if found, or tries assuming the role of the executing
machine if not.

## Error handling

Refer [Error handling].

Exceptions one might encounter when using Boto3 will come from botocore or from the AWS service one's client is
interacting with.

Exceptions from botocore are statically defined within the `botocore` package, which Boto3 depends upon.<br/>
Definitions [here][boto/botocore/exceptions.py].

<details style="padding: 0 0 1em 1em">
  <summary>Generate a list of botocore's <b>statically</b> defined exceptions</summary>

```py
import botocore.exceptions

for key, value in sorted(botocore.exceptions.__dict__.items()):
    if isinstance(value, type):
        print(key)
```

</details>

Exceptions from AWS services are **not** statically defined in Boto3 and must be caught through botocore's `ClientError`
exception.<br/>
Catch this exception, then parse through the response for specifics around that error.

Consult the service's API reference on AWS for a complete list of error responses made available from that service.

One can also access **some** of the dynamic service-side exceptions from the client's exception property.

<details style="padding: 0 0 0 1em">
  <summary>Clients</summary>

```diff
 import boto3
-from botocore.exceptions import ClientError, ParamValidationError

 client = boto3.client('kinesis')
 try:
     client.describe_stream(StreamName='myDataStream')
+except client.exceptions.LimitExceedException as e:
+    print('API call limit exceeded; backing off and retrying...')
-except ClientError as e:
-    if error.response['Error']['Code'] == 'LimitExceededException':
-        print('API call limit exceeded; backing off and retrying...')
-    else:
-        raise e
```

</details>

<details style="padding: 0 0 1em 1em">
  <summary>Resources</summary>

```diff
 import boto3
-from botocore.exceptions import ClientError, ParamValidationError

 client = boto3.resource('s3')
 try:
     client.create_bucket(BucketName='amzn-s3-demo-bucket')
+except client.meta.client.exceptions.BucketAlreadyExists as e:
+    print(f"Bucket {e.response['Error']['BucketName']} already exists")
-except ClientError as e:
-    if error.response['Error']['Code'] == 'BucketAlreadyExists':
-        print('Bucket already exists')
-    else:
-        raise e
```

</details>

## Further readings

- [Boto3 documentation]
- [More info about resource deprecation?]
- [Paginators]

### Sources

- [Resources]
- [Sessions]
- [Error handling]
- [How to handle errors with boto3?]

<!--
  Reference
  ═╬═Time══
  -->

<!-- Upstream -->
[error handling]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/error-handling.html
[boto/botocore/exceptions.py]: https://github.com/boto/botocore/blob/develop/botocore/exceptions.py
[boto3 documentation]: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
[paginators]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html
[resources]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html
[more info about resource deprecation?]: https://github.com/boto/boto3/discussions/3563
[sessions]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html

<!-- Others -->
[how to handle errors with boto3?]: https://stackoverflow.com/questions/33068055/how-to-handle-errors-with-boto3#33663484
