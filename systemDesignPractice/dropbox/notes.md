# dropbox system design notes

Used requirements from here: https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox

## Function requirements
- Users should be able to upload a file from any device
- Users should be able to download a file from any device
- Users should be able to share a file with other users and view the files shared with them
- Users can automatically sync files across devices

- **NOT** worrying about editing files and viewing without download

## Non-Function requirements
- The system should be highly available (prioritizing availability over consistency).
- The system should support files as large as 50GB.
- The system should be secure and reliable. We should be able to recover files if they are lost or corrupted.
- The system should make upload, download, and sync times as fast as possible (low latency).

## Immediate thoughts
- File storage is a blob storage, but the files will need metadata
  - The metadata can be in a NoSQL DB
- We want to prioritize availability so horizontal scaling can help with that
- security can be provided through auth from JWT, auth0, something like that
- The metadata can contain IDs for users who can see the file (for sharing)
- download can be done through a CDN using some kind of key?

## API

1. POST - upload a file and store that
2. GET - download a file
3. PATCH - share the file
4. PUT - syncing files 


## Design notes
- The user sends a request to the load balancer, and they go to the services that are horizontally scaled; 
this provides the necessary availability
- Files are stored in blob storage and the metadata in a NoSQL DB, this allows custom metadata 
and flexibility with fields
- Downloads are provided through a CDN, each time a file is uploaded a CDN link is provided
  -  this also gives the security and reliability we need for the downloads
- The metadata can contain IDs for who has access that can be checked
- DB's should also be shared for availability and storage needs
- Syncing files can be a SSE like a PUT request to update the files?

## Review thoughts & research into other solutions
- A separate table for sharing files would be better because keeping the share in the files metadata
would be a slow query to make
- A relational DB would be better for speed and following a structure like folders
- Changes to files would be huge requests, so breaking files down blocks could make the requests smaller
- Could add a polling service that checks the blob for files that aren't being accessed and places 
them into cold storage
   - this would speed up retrieval for new/frequent files and save on costs at the cost of 
   slow speed for when they are finally used
- Recently added files could have their metadata in a cache instead for speed
