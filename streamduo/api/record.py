import json
from enum import Enum


class RecordController:

    def __init__(self, client):
        self.client = client

    def write_record(self, stream_id, json_payload, record_id=None):
        record = Record()
        record.recordId = record_id
        if isinstance(json_payload, str):
            record.dataPayload = json_payload
        else:
            record.dataPayload = json.dumps(json_payload)
        return self.client.call_api("POST",
                             f"/stream/{stream_id}/record/",
                             body=record.to_json()
                             )

    def write_csv_records(self, stream_id, file_stream):
        file_payload = {'file': file_stream}
        return self.client.call_api("POST",
                             f"/stream/{stream_id}/record/batch-file",
                                    files=file_payload
                             )

    def read_record(self, stream_id, record_id, mark_as_read):
        read_record_request = ReadRecordRequest()
        read_record_request.recordId = record_id
        read_record_request.readRecordRequestType = ReadRecordRequestType.SINGLE
        read_record_request.markAsRead = mark_as_read
        read_record_request.recordCount = 1
        return self._read_record_request(stream_id, read_record_request)

    def read_record_hist(self, stream_id, record_id, count, mark_as_read):
        read_record_request = ReadRecordRequest()
        read_record_request.recordId = record_id
        read_record_request.readRecordRequestType = ReadRecordRequestType.SINGLE
        read_record_request.markAsRead = mark_as_read
        read_record_request.recordCount = count
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


class Record:

     def __init__(self):
         self.recordId = None
         self.streamId = None
         self.recordTimeStampISO = None
         self.readStatus = None
         self.dataPayload = None
     def to_json(self):
         return self.__dict__