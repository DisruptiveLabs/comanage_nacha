from .file_header import FileHeader
from .company_batch_header import CompanyBatchHeader
from .entry_detail import EntryDetail
from .entry_addenda import EntryAddenda
from .company_batch_control import CompanyBatchControl
from .file_control import FileControl

entry_types = {
    FileHeader.code: FileHeader,
    CompanyBatchHeader.code: CompanyBatchHeader,
    EntryDetail.code: EntryDetail,
    EntryAddenda.code: EntryAddenda,
    CompanyBatchControl.code: CompanyBatchControl,
    FileControl.code: FileControl,
}
