from enum import Enum


class Record:

    def __init__(self, client):
        self.client = client

    def write_record(self, stream_id, json_payload):
        return self.client.call_api("POST",
                             f"/stream/{stream_id}/record/",
                             body=json_payload
                             )

    def read_record(self, stream_id, record_id, mark_as_read):
        read_record_request = ReadRecordRequest()
        read_record_request.recordId = record_id
        read_record_request.readRecordRequestType = ReadRecordRequestType.SINGLE
        read_record_request.markAsRead = mark_as_read
        return self._read_record_request(stream_id, read_record_request)

    def read_unread_records(self, stream_id, mark_as_read, record_count):
        read_record_request = ReadRecordRequest()
        read_record_request.readRecordRequestType = ReadRecordRequestType.UNREAD
        read_record_request.markAsRead = mark_as_read
        read_record_request.recordCount = record_count
        return self._read_record_request(stream_id, read_record_request)

    def read_last_n_records(self, stream_id, mark_as_read, record_count):
        read_record_request = ReadRecordRequest()
        read_record_request.readRecordRequestType = ReadRecordRequestType.LAST_N
        read_record_request.markAsRead = mark_as_read
        read_record_request.recordCount = record_count
        return self._read_record_request(stream_id, read_record_request)

    def read_records_since_timestamp(self, stream_id, timestamp, mark_as_read, record_count):
        read_record_request = ReadRecordRequest()
        read_record_request.readRecordRequestType = ReadRecordRequestType.READ_SINCE_TIMESTAMP
        read_record_request.recordTimeStampISO = timestamp
        read_record_request.markAsRead = mark_as_read
        read_record_request.recordCount = record_count
        return self._read_record_request(stream_id, read_record_request)

    def _read_record_request(self, stream_id, read_record_request):
        read_record_request.readRecordRequestType = read_record_request.readRecordRequestType.value
        return self.client.call_api("POST",
                             f"/stream/{stream_id}/record-request",
                             body=read_record_request.to_json()
                             )


class ReadRecordRequest:

     def __init__(self):
         self.readRecordRequestType = None
         self.recordCount = None
         self.recordId = None
         self.markAsRead = None
         self.recordTimeStampISO = None
     def to_json(self):
         return self.__dict__

class ReadRecordRequestType(Enum):
    SAMPLE = 'SAMPLE'
    UNREAD = 'UNREAD'
    READ_SINCE_RECORD_ID = 'READ_SINCE_RECORD_ID'
    READ_SINCE_TIMESTAMP = 'READ_SINCE_TIMESTAMP'
    SINGLE = 'SINGLE'
    LAST_N = 'LAST_N'