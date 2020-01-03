""" contains all exceptions raised for package """

NoFileOrDir = ValueError('Must specify a file or directory')

NotAvscFileError = ValueError()

MissingFileError = OSError()

NoFilesError = OSError

BadReferenceError = ValueError(
    'field to be referenced missing namespace or name keys'
)
