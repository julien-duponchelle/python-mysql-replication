# Last event of a statement
FLAG_STMT_END_F = 1 << 0
# Value of the OPTION_NO_FOREIGN_KEY_CHECKS flag in thd->options
FLAG_NO_FOREIGN_KEY_CHECKS_F = 1 << 1
# Value of the OPTION_RELAXED_UNIQUE_CHECKS flag in thd->options
FLAG_RELAXED_UNIQUE_CHECKS_F = 1 << 2
#
# Indicates that rows in this event are complete, that is contain
# values for all columns of the table.
#
FLAG_COMPLETE_ROWS_F = 1 << 3
