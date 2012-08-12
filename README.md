# python3-ccr

CCR Library for Python 3

## Usage
When using this library you must first decide whether you will use Redis or not. It will be imported not matter what but you can choose to use or not use it.
If you do decide to use it you will need to have an instance of the RedisCCR class: `redis_ccr = RedisCCR()`

The following instructions will be using the redis database only with the instance name `redis_ccr`

## Basic Functions
Search*: `redis_ccr.search('keyword')`
Info: `redis_ccr.info('package')`
Maintainer Search: `redis_ccr.msearch('maintainer')`
CCR URL: `redis_ccr.geturl('package')`
Orphan List: `redis_ccr.orphans()`

* Search with redis doesn't search descriptions. To search descriptions use searchRemote()
