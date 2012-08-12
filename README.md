# python3-ccr

CCR Library for Python 3

## Usage
When using this library you must first decide whether you will use Redis or not. It will be imported not matter what but you can choose to use or not use it.
If you do decide to use it you will need to have an instance of the RedisCCR class: `redis_ccr = RedisCCR()`

In order to use non-redis functions just add Remote to the end of the name (so `RedisCCR.search()` would be `searchRemote()`)

The following instructions will be using the redis database only with the instance name `redis_ccr`

#### Basic Functions
Search: `redis_ccr.search('keyword')`

Info: `redis_ccr.info('package')`

Maintainer Search: `redis_ccr.msearch('maintainer')`

CCR URL: `redis_ccr.geturl('package')`

Orphan List: `redis_ccr.orphans()`

Get Latest Packages: `getlatest(num=20)`

Download Package: `getpkg('package', 'destinationfile')`

Search with redis doesn't search descriptions. To search descriptions use searchRemote()

#### Redis-Specific Functions
`redis_ccr.needsUpdate()` returns a bool which tells whether the data has expired in the database and `redis_ccr.updatePackages()` refreshes the data.

#### Other Functions
To be written

### Classes
#### CCRSession()
This class has all the actions that can be preformed on the CCR. You must have a username and password for the CCR to use it.

To begin using it create a new instance: `session = CCRSession('username', 'password')` Optionally, you can add use_redis=False if the redis database should not be used.

The current actions are: `flag`, `unflag`, `vote`, `unvote`, `notify`, `unnotify`, `delete`, `adopt`, `disown`, and `setcategory`
The current information functions are: `getid` and `voted`
