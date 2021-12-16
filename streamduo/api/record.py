import json

from streamduo.models.read_record_request import ReadRecordRequest
from streamduo.models.record import Record
from streamduo.models.record_request import ReadRecordRequestType


class RecordController:
    """
    This class manages the reading and writing of records to streams.
    """

    def __init__(self, client):
        self.client = client

    def write_record(self, stream_id, json_payload, record_id=None):
        """
        Writes a single record to the stream.
        :param stream_id: (String) Stream ID to write to
        :param json_payload: (Dict OR JSON formatted String) The payload of the record
        :param record_id: (String) OPTIONAL - Used in the case you want to force a particular record ID.
        If left null, record ID will be generated by API
        :return: (Requests Response) API response, body will be a Record object Dict.
        """
        record = Record()
        record.recordId = record_id
        if isinstance(json_payload, str):
            record.dataPayload = json.loads(json_payload)
        else:
            record.dataPayload = json_payload
        return self.client.call_api("POST",
                                    f"/stream/{stream_id}/record",
                                    body=record.to_json()
                                    )



    def write_csv_records(self, stream_id, file_stream):
        """
        Writes a CSV file of records to a stream.
        :param stream_id: (String) Stream ID to write to
        :param file_stream: (File) File Object of CSV
        :return:  (Requests Response) API response, body will be a String detailing the status.
        """
        file_payload = {'file': file_stream}
        return self.client.call_api("POST",
                                    f"/stream/{stream_id}/record/batch-file",
                                    files=file_payload
                                    )

    def read_record(self, stream_id, record_id, mark_as_read):
        """
        Reads the latest version of a specific record in a stream by Record ID
        :param stream_id: (String) Stream to read from
        :param record_id: (String) Record ID to read
        :param mark_as_read: (Bool) Whether the record should be marked as read
        :return:  (Requests Response) API response, body will be LIST of Record object Dicts.
        """
        read_record_request = ReadRecordRequest()
        read_record_request.recordId = record_id
        read_record_request.readRecordRequestType = ReadRecordRequestType.SINGLE
        read_record_request.markAsRead = mark_as_read
        read_record_request.recordCount = 1
        return self._read_record_request(stream_id, read_record_request)

    def read_record_hist(self, stream_id: str, record_id: str, count: int, mark_as_read: bool):
        """
        Reads historical records from a stream, for a given record ID.
        :param stream_id: (String) Stream to read from
        :param record_id: (String) Record ID to read
        :param count: (Int) Number of historical records to read for (going back in time)
        :param mark_as_read: (Bool) Whether the record should be marked as read
        :return:  (Requests Response) API response, body will be LIST of Record object Dicts.
        """

        read_record_request = ReadRecordRequest()
        read_record_request.recordId = record_id
        read_record_request.readRecordRequestType = ReadRecordRequestType.SINGLE
        read_record_request.markAsRead = mark_as_read
        read_record_request.recordCount = count
        return self._read_record_request(stream_id, read_record_request)

    def read_unread_records(self, stream_id, mark_as_read, record_count):
        """
        Reads unread records from a stream, returning records in chronological order
        from the last read record.
        :param stream_id: (String) Stream to read from
        :param mark_as_read: (Bool) Whether the record should be marked as read
        :param record_count: (Int) Number of records to read
        :return: (Requests Response) API response, body will be LIST of Record object Dicts.
        """
        read_record_request = ReadRecordRequest()
        read_record_request.readRecordRequestType = ReadRecordRequestType.UNREAD
        read_record_request.markAsRead = mark_as_read
        read_record_request.recordCount = record_count
        return self._read_record_request(stream_id, read_record_request)

    def read_last_n_records(self, stream_id, mark_as_read, record_count):
        """
        Reads the last {record_count} records in a stream
        :param stream_id: (String) Stream to read from
        :param mark_as_read:  (Bool) Whether the record should be marked as read
        :param record_count: (Int) Number of records to read
        :return: (Requests Response) API response, body will be LIST of Record object Dicts.
        """
        read_record_request = ReadRecordRequest()
        read_record_request.readRecordRequestType = ReadRecordRequestType.LAST_N
        read_record_request.markAsRead = mark_as_read
        read_record_request.recordCount = record_count
        return self._read_record_request(stream_id, read_record_request)

    def read_records_since_timestamp(self, stream_id, timestamp, mark_as_read, record_count):
        """
        Reads records in stream since a given timestamp
        :param stream_id: (String) Stream to read from
        :param timestamp: (String) Timestamp to start reading from (ISO format) i.e. 2021-11-03T21:03
        :param mark_as_read: (Bool) Whether the record should be marked as read
        :param record_count: (Int) Number of records to read
        :return: (Requests Response) API response, body will be LIST of Record object Dicts.
        """
        read_record_request = ReadRecordRequest()
        read_record_request.readRecordRequestType = ReadRecordRequestType.READ_SINCE_TIMESTAMP
        read_record_request.recordTimeStampISO = timestamp
        read_record_request.markAsRead = mark_as_read
        read_record_request.recordCount = record_count
        return self._read_record_request(stream_id, read_record_request)

    def _read_record_request(self, stream_id, read_record_request):
        """
        Internal method for executing the read records request
        :param stream_id: (String) Stream Id to read from
        :param read_record_request: (ReadRecordRequest) object representing the read records request
        :return: (Requests Response) API response, body will be LIST of Record object Dicts.
        """
        read_record_request.readRecordRequestType = read_record_request.readRecordRequestType.value
        return self.client.call_api("POST",
                                    f"/stream/{stream_id}/record-request",
                                    body=read_record_request.to_json
                                    )


