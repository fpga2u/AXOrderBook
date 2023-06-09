#include "axob_mu.hpp"

#include "sbe_intf.hpp"
#include "sbe_ssz_origin.hpp"
#include "dbg_info.hpp"
void axob_mu(
	/* register-from-host */
	unsigned int    reg_securityID_idx_i,        //index of securityID
	/* register-to-host */
	//---- upstream ----
	unsigned int&    reg_order_nb_o,               //nb of order
	unsigned int&    reg_exec_nb_o,                //nb of exec
	unsigned int&    reg_snap_nb_o,                //nb of snap
	unsigned int&    reg_unknown_nb_o,             //nb of unknown frame
	unsigned int&    reg_frame_bytes_cnt_o,        //nb of bytes of all sbe frames
	unsigned int&    reg_frame_head_o,             //begin word of last read frame
	unsigned int&    reg_frame_type_o,             //message type of last read frame
	unsigned int&    reg_frame_tail_o,             //end word of last read frame
	//---- stats of MU ----
	unsigned int&    reg_ChannelNo_o,              //end word of last read frame
	unsigned int&    reg_TPM_o,                    //end word of last read frame
	//---- stats of securityID ----
	unsigned int&    reg_securityID_nb_o,          //nb of managed SecurityIDs
	unsigned int&    reg_sID_var_o,                //variable of [index of securityID]
	unsigned int&    reg_sID_order_nb_o,           //nb of order of [index of securityID]
	unsigned int&    reg_sID_exec_nb_o,            //nb of exec of [index of securityID]
	unsigned int&    reg_sID_snap_nb_o,            //nb of snap of [index of securityID]
	unsigned int&    reg_sID_snapGen_nb_o,         //nb of generated snap of [index of securityID]
	/* memory */
	/* stream */
	//---- data-from-upstream ----
	signal_stream_t&    signal_stream_i,          //Stream from XV: signal
	sbe_stream::stream_t&    sbe_stream_i,        //Stream from XV: sbe
	//---- data-to-downstream ----
	signal_stream_t&    signal_stream_o,          //Stream to XV: signal
	sbe_stream::stream_t&    sbe_stream_o         //Stream to XV: snap-gen
)
{
	/* define register-to-host */
	//---- upstream ----
	static unsigned int    _reg_order_nb_o=0;               //nb of order
	static unsigned int    _reg_exec_nb_o=0;                //nb of exec
	static unsigned int    _reg_snap_nb_o=0;                //nb of snap
	static unsigned int    _reg_unknown_nb_o=0;             //nb of unknown frame
	static unsigned int    _reg_frame_bytes_cnt_o=0;        //nb of bytes of all sbe frames
	static unsigned int    _reg_frame_head_o=0;             //begin word of last read frame
	static unsigned int    _reg_frame_type_o=0;             //message type of last read frame
	static unsigned int    _reg_frame_tail_o=0;             //end word of last read frame
	//---- stats of MU ----
	static unsigned int    _reg_ChannelNo_o=0;              //end word of last read frame
	static unsigned int    _reg_TPM_o=0;                    //end word of last read frame
	//---- stats of securityID ----
	static unsigned int    _reg_securityID_nb_o=0;          //nb of managed SecurityIDs
	static unsigned int    _reg_sID_var_o=0;                //variable of [index of securityID]
	static unsigned int    _reg_sID_order_nb_o=0;           //nb of order of [index of securityID]
	static unsigned int    _reg_sID_exec_nb_o=0;            //nb of exec of [index of securityID]
	static unsigned int    _reg_sID_snap_nb_o=0;            //nb of snap of [index of securityID]
	static unsigned int    _reg_sID_snapGen_nb_o=0;         //nb of generated snap of [index of securityID]




	/* update register-to-host */
	//---- upstream ----
	reg_order_nb_o = _reg_order_nb_o;                      //nb of order
	reg_exec_nb_o = _reg_exec_nb_o;                        //nb of exec
	reg_snap_nb_o = _reg_snap_nb_o;                        //nb of snap
	reg_unknown_nb_o = _reg_unknown_nb_o;                  //nb of unknown frame
	reg_frame_bytes_cnt_o = _reg_frame_bytes_cnt_o;        //nb of bytes of all sbe frames
	reg_frame_head_o = _reg_frame_head_o;                  //begin word of last read frame
	reg_frame_type_o = _reg_frame_type_o;                  //message type of last read frame
	reg_frame_tail_o = _reg_frame_tail_o;                  //end word of last read frame
	//---- stats of MU ----
	reg_ChannelNo_o = _reg_ChannelNo_o;                    //end word of last read frame
	reg_TPM_o = _reg_TPM_o;                                //end word of last read frame
	//---- stats of securityID ----
	reg_securityID_nb_o = _reg_securityID_nb_o;            //nb of managed SecurityIDs
	reg_sID_var_o = _reg_sID_var_o;                        //variable of [index of securityID]
	reg_sID_order_nb_o = _reg_sID_order_nb_o;              //nb of order of [index of securityID]
	reg_sID_exec_nb_o = _reg_sID_exec_nb_o;                //nb of exec of [index of securityID]
	reg_sID_snap_nb_o = _reg_sID_snap_nb_o;                //nb of snap of [index of securityID]
	reg_sID_snapGen_nb_o = _reg_sID_snapGen_nb_o;          //nb of generated snap of [index of securityID]

	return;

}