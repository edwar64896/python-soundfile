import os
import sys
from cffi import FFI

ffibuilder = FFI()
ffibuilder.set_source("_soundfile", None)
ffibuilder.cdef("""
                
//typedef	short int16_t;
//typedef	unsigned short uint16_t;              
//typedef int	int32_t;
//typedef unsigned int uint32_t;
//typedef	long int64_t;
                
enum
{
    SF_FORMAT_SUBMASK       = 0x0000FFFF,
    SF_FORMAT_TYPEMASK      = 0x0FFF0000,
    SF_FORMAT_ENDMASK       = 0x30000000
} ;

enum
{
    SFC_GET_LIB_VERSION=              0x1000,
	SFC_GET_LOG_INFO=                 0x1001,
	SFC_GET_CURRENT_SF_INFO=          0x1002,
	SFC_GET_NORM_DOUBLE=              0x1010,
	SFC_GET_NORM_FLOAT=               0x1011,
	SFC_SET_NORM_DOUBLE=              0x1012,
	SFC_SET_NORM_FLOAT=               0x1013,
	SFC_SET_SCALE_FLOAT_INT_READ=     0x1014,
	SFC_SET_SCALE_INT_FLOAT_WRITE=    0x1015,

	SFC_GET_SIMPLE_FORMAT_COUNT=      0x1020,
	SFC_GET_SIMPLE_FORMAT=            0x1021,

	SFC_GET_FORMAT_INFO=              0x1028,

	SFC_GET_FORMAT_MAJOR_COUNT=       0x1030,
	SFC_GET_FORMAT_MAJOR=             0x1031,
	SFC_GET_FORMAT_SUBTYPE_COUNT=     0x1032,
	SFC_GET_FORMAT_SUBTYPE=           0x1033,

	SFC_CALC_SIGNAL_MAX=              0x1040,
	SFC_CALC_NORM_SIGNAL_MAX=         0x1041,
	SFC_CALC_MAX_ALL_CHANNELS=        0x1042,
	SFC_CALC_NORM_MAX_ALL_CHANNELS=   0x1043,
	SFC_GET_SIGNAL_MAX=               0x1044,
	SFC_GET_MAX_ALL_CHANNELS=         0x1045,

	SFC_SET_ADD_PEAK_CHUNK=           0x1050,

	SFC_UPDATE_HEADER_NOW=            0x1060,
	SFC_SET_UPDATE_HEADER_AUTO=       0x1061,

	SFC_FILE_TRUNCATE=                0x1080,

	SFC_SET_RAW_START_OFFSET=         0x1090,

	/*Commands reserved for dithering, which is not implemented.*/
	SFC_SET_DITHER_ON_WRITE=          0x10A0,
	SFC_SET_DITHER_ON_READ=           0x10A1,

	SFC_GET_DITHER_INFO_COUNT=        0x10A2,
	SFC_GET_DITHER_INFO=              0x10A3,

	SFC_GET_EMBED_FILE_INFO=          0x10B0,

	SFC_SET_CLIPPING=                 0x10C0,
	SFC_GET_CLIPPING=                 0x10C1,

	SFC_GET_CUE_COUNT=                0x10CD, 
	SFC_GET_CUE=                      0x10CE,
	SFC_SET_CUE=                      0x10CF,

	SFC_GET_INSTRUMENT=               0x10D0,
	SFC_SET_INSTRUMENT=               0x10D1,

	SFC_GET_LOOP_INFO=                0x10E0,

	SFC_GET_BROADCAST_INFO=           0x10F0,
	SFC_SET_BROADCAST_INFO=           0x10F1,

	SFC_GET_CHANNEL_MAP_INFO=         0x1100,
	SFC_SET_CHANNEL_MAP_INFO=         0x1101,

	SFC_RAW_DATA_NEEDS_ENDSWAP=       0x1110,

	/*Support for Wavex Ambisonics Format */
	SFC_WAVEX_SET_AMBISONIC=          0x1200,
	SFC_WAVEX_GET_AMBISONIC=          0x1201,

	SFC_RF64_AUTO_DOWNGRADE=          0x1210,

	SFC_SET_VBR_ENCODING_QUALITY=     0x1300,
	SFC_SET_COMPRESSION_LEVEL=        0x1301,

	/* Ogg format commands */
	SFC_SET_OGG_PAGE_LATENCY_MS=      0x1302,
	SFC_SET_OGG_PAGE_LATENCY=         0x1303,
	SFC_GET_OGG_STREAM_SERIALNO=      0x1306,

	SFC_GET_BITRATE_MODE=             0x1304,
	SFC_SET_BITRATE_MODE=             0x1305,

	/* Cart Chunk support */
	SFC_SET_CART_INFO=                0x1400,
	SFC_GET_CART_INFO=                0x1401,

	/* Opus files original samplerate metadata */
	SFC_SET_ORIGINAL_SAMPLERATE=      0x1500,
	SFC_GET_ORIGINAL_SAMPLERATE=      0x1501,

	/* Following commands for testing only. */
	SFC_TEST_IEEE_FLOAT_REPLACE=      0x6001,

	SFC_SET_ADD_HEADER_PAD_CHUNK=     0x1051,

	SFC_SET_ADD_DITHER_ON_WRITE=      0x1070,
	SFC_SET_ADD_DITHER_ON_READ=       0x1071
} ;

enum
{
    SF_FALSE    = 0,
    SF_TRUE     = 1,

    /* Modes for opening files. */
    SFM_READ    = 0x10,
    SFM_WRITE   = 0x20,
    SFM_RDWR    = 0x30,
} ;

typedef int64_t sf_count_t ;

typedef struct SNDFILE_tag SNDFILE ;

struct SF_CHUNK_ITERATOR
{	unsigned int	current ;
	long		hash ;
	char		id [64] ;
	unsigned	id_size ;
	SNDFILE		*sndfile ;
} ;      

typedef	struct SF_CHUNK_ITERATOR SF_CHUNK_ITERATOR ;         

struct SF_CHUNK_INFO
{	char		id [64] ;	/* The chunk identifier. */
	unsigned	id_size ;	/* The size of the chunk identifier. */
	unsigned	datalen ;	/* The size of that data. */
	void		*data ;		/* Pointer to the data. */
} ;

typedef struct SF_CHUNK_INFO SF_CHUNK_INFO ;

typedef struct SF_INFO
{
    sf_count_t frames ;        /* Used to be called samples.  Changed to avoid confusion. */
    int        samplerate ;
    int        channels ;
    int        format ;
    int        sections ;
    int        seekable ;
} SF_INFO ;

SNDFILE*    sf_open          (const char *path, int mode, SF_INFO *sfinfo) ;
int         sf_format_check  (const SF_INFO *info) ;

sf_count_t  sf_seek          (SNDFILE *sndfile, sf_count_t frames, int whence) ;

int         sf_command       (SNDFILE *sndfile, int cmd, void *data, int datasize) ;

int         sf_error         (SNDFILE *sndfile) ;
const char* sf_strerror      (SNDFILE *sndfile) ;
const char* sf_error_number  (int errnum) ;

int         sf_perror        (SNDFILE *sndfile) ;
int         sf_error_str     (SNDFILE *sndfile, char* str, size_t len) ;

int         sf_close         (SNDFILE *sndfile) ;
void        sf_write_sync    (SNDFILE *sndfile) ;

sf_count_t  sf_read_short    (SNDFILE *sndfile, short *ptr, sf_count_t items) ;
sf_count_t  sf_read_int      (SNDFILE *sndfile, int *ptr, sf_count_t items) ;
sf_count_t  sf_read_float    (SNDFILE *sndfile, float *ptr, sf_count_t items) ;
sf_count_t  sf_read_double   (SNDFILE *sndfile, double *ptr, sf_count_t items) ;

/* Note: Data ptr argument types are declared as void* here in order to
         avoid an implicit cast warning. (gh183). */
sf_count_t  sf_readf_short   (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_readf_int     (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_readf_float   (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_readf_double  (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;

sf_count_t  sf_write_short   (SNDFILE *sndfile, short *ptr, sf_count_t items) ;
sf_count_t  sf_write_int     (SNDFILE *sndfile, int *ptr, sf_count_t items) ;
sf_count_t  sf_write_float   (SNDFILE *sndfile, float *ptr, sf_count_t items) ;
sf_count_t  sf_write_double  (SNDFILE *sndfile, double *ptr, sf_count_t items) ;

/* Note: The argument types were changed to void* in order to allow
         writing bytes in SoundFile.buffer_write() */
sf_count_t  sf_writef_short  (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_writef_int    (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_writef_float  (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;
sf_count_t  sf_writef_double (SNDFILE *sndfile, void *ptr, sf_count_t frames) ;

sf_count_t  sf_read_raw      (SNDFILE *sndfile, void *ptr, sf_count_t bytes) ;
sf_count_t  sf_write_raw     (SNDFILE *sndfile, void *ptr, sf_count_t bytes) ;

const char* sf_get_string    (SNDFILE *sndfile, int str_type) ;
int         sf_set_string    (SNDFILE *sndfile, int str_type, const char* str) ;
const char * sf_version_string (void) ;

typedef sf_count_t  (*sf_vio_get_filelen) (void *user_data) ;
typedef sf_count_t  (*sf_vio_seek)        (sf_count_t offset, int whence, void *user_data) ;
typedef sf_count_t  (*sf_vio_read)        (void *ptr, sf_count_t count, void *user_data) ;
typedef sf_count_t  (*sf_vio_write)       (const void *ptr, sf_count_t count, void *user_data) ;
typedef sf_count_t  (*sf_vio_tell)        (void *user_data) ;

typedef struct SF_VIRTUAL_IO
{    sf_count_t  (*get_filelen) (void *user_data) ;
     sf_count_t  (*seek)        (sf_count_t offset, int whence, void *user_data) ;
     sf_count_t  (*read)        (void *ptr, sf_count_t count, void *user_data) ;
     sf_count_t  (*write)       (const void *ptr, sf_count_t count, void *user_data) ;
     sf_count_t  (*tell)        (void *user_data) ;
} SF_VIRTUAL_IO ;

SNDFILE*    sf_open_virtual   (SF_VIRTUAL_IO *sfvirtual, int mode, SF_INFO *sfinfo, void *user_data) ;
SNDFILE*    sf_open_fd        (int fd, int mode, SF_INFO *sfinfo, int close_desc) ;
                
SF_CHUNK_ITERATOR * sf_get_chunk_iterator (SNDFILE * sndfile, const SF_CHUNK_INFO * chunk_info) ;       
SF_CHUNK_ITERATOR * sf_next_chunk_iterator (SF_CHUNK_ITERATOR * iterator) ;     
int                 sf_get_chunk_size (const SF_CHUNK_ITERATOR * it, SF_CHUNK_INFO * chunk_info) ;                    
int                 sf_get_chunk_data (const SF_CHUNK_ITERATOR * it, SF_CHUNK_INFO * chunk_info) ;
                
typedef struct SF_FORMAT_INFO
{
    int         format ;
    const char* name ;
    const char* extension ;
} SF_FORMAT_INFO ;
                
typedef struct SF_BROADCAST_INFO 
	{	
        char		description [256] ;
		char		originator [32] ;
		char		originator_reference [32] ;
		char		origination_date [10] ;
		char		origination_time [8] ;
		unsigned int	time_reference_low ;
		unsigned int	time_reference_high ;
		short		version ;
		char		umid [64] ;
		short	loudness_value ;
		short	loudness_range ;
		short	max_true_peak_level ;
		short	max_momentary_loudness ;
		short	max_shortterm_loudness ;
		char		reserved [180] ;
		unsigned int	coding_history_size ;
		char		coding_history [256] ;
	} SF_BROADCAST_INFO;

typedef struct SF_CART_TIMER
{	char	usage [4] ;
	unsigned int	value ;
} SF_CART_TIMER;

typedef struct SF_CART_INFO
	{	
        char		version [4] ;
		char		title [64] ;
		char		artist [64] ;
		char		cut_id [64] ;
		char		client_id [64] ;
		char		category [64] ;
		char		classification [64] ;
		char		out_cue [64] ;
		char		start_date [10] ;
		char		start_time [8] ;
		char		end_date [10] ;
		char		end_time [8] ;
		char		producer_app_id [64] ;
		char		producer_app_version [64] ;
		char		user_def [64] ;
		int		level_reference ;
		SF_CART_TIMER	post_timers [8] ;
		char		reserved [276] ;
		char		url [1024] ;
		unsigned int	tag_text_size ;
		char		tag_text [256] ;
	} SF_CART_INFO;
                


                
typedef struct SF_LOOP_INFO
{
	short	time_sig_num ;	/* any positive integer    > 0  */
	short	time_sig_den ;	/* any positive power of 2 > 0  */
	int		loop_mode ;		/* see SF_LOOP enum             */

	int		num_beats ;		/* this is NOT the amount of quarter notes !!!*/
							/* a full bar of 4/4 is 4 beats */
							/* a full bar of 7/8 is 7 beats */

	float	bpm ;			/* suggestion, as it can be calculated using other fields:*/
							/* files length, files sampleRate and our time_sig_den*/
							/* -> bpms are always the amount of _quarter notes_ per minute */

	int	root_key ;			/* MIDI note, or -1 for None */
	int future [6] ;
} SF_LOOP_INFO ;
                
typedef struct SF_INSTRUMENT
{	int gain ;
	char basenote, detune ;
	char velocity_lo, velocity_hi ;
	char key_lo, key_hi ;
	int loop_count ;

	struct
	{	int mode ;
		unsigned int start ;
		unsigned int end ;
		unsigned int count ;
	} loops [16] ; /* make variable in a sensible way */
} SF_INSTRUMENT ;
                
typedef struct SF_CUE_POINT
{	int 	indx ;
	unsigned int position ;
	int 	fcc_chunk ;
	int 	chunk_start ;
	int		block_start ;
	unsigned int 	indx ;
 	unsigned int	sample_offset ;
	char name [256] ;
} SF_CUE_POINT ;
                
typedef struct SF_CUES
	{	unsigned int cue_count ;
		SF_CUE_POINT cue_points [100] ;
	} SF_CUES;

""")

platform = os.environ.get('PYSOUNDFILE_PLATFORM', sys.platform)
if platform == 'win32':
    ffibuilder.cdef("""
    SNDFILE* sf_wchar_open (const wchar_t *wpath, int mode, SF_INFO *sfinfo) ;
    """)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
