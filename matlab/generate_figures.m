function results_listing = generate_figures(dir_list, dBRange)
    % Check if dBRange has been given as input
    if ~exist('dBRange', 'var')
        dBRange = 60;
    end

    % Add PICMUS path
    addpath(genpath('picmus'));
    
    % Load the scan object
    url = 'https://www.creatis.insa-lyon.fr/EvaluationPlatform/picmus/dataset/';
    picmus_scan_path = '../data/picmus17/';
    scan_filename = 'scanning_region_picmus.hdf5';
    
    %-- create the scan object
    scan = linear_scan();
    scan.read_file(fullfile(picmus_scan_path, scan_filename));
    
    for ll = 1:numel(dir_list)
        dir_name = dir_list{ll};
        % Get a listing of all the .mat files in dir_name
        results_listing=dir(fullfile(dir_name,'*.mat'));
        
        % Generate a report for each file in dir_name
        for kk = 1:size(results_listing,1)
            cur_list = results_listing(kk,:);
            
            if not(contains(cur_list.name, 'metrics'))
                % Load the filename from the current list
                file_name = fullfile(cur_list.folder, cur_list.name);
                load(file_name);

                disp(['************ ', cur_list.name, ' ************'])
                % Take the envelope of the RF image and interpolate on the scan
                envelope = tools.envelope(rf_data);
                [Xim, Zim] = meshgrid(xim ,zim);
                reshaped_envelope =interp2(Xim, Zim , envelope, scan.x_matrix, scan.z_matrix, 'linear', 0);

                % Take the B-mode image
                bmode = reshaped_envelope / max(reshaped_envelope(:));
                bmode_compressed = 20*log10(bmode);
                bmode_compressed(bmode_compressed < -dBRange) = -dBRange;
                
                % Store the envelope in image object
                h=figure('Color', 'None');
                imagesc(scan.x*1000, scan.z*1000, bmode_compressed); colormap gray; axis image;
                h2 = colorbar;
                set(h2,'YTick',-dBRange:10:0);
                set(h2,'YTickLabel',{'-60 dB'; '-50 dB'; '-40 dB';'-30 dB';'-20 dB';'-10 dB';'0 dB'});
                caxis([-dBRange, 0]);
                xlabel 'Lateral dimension [mm]'
                ylabel 'Depth [mm]'
                set(gca,'fontsize',16);
                
                % Export the figures in eps
                format = '.mat';
                fig_format = '.eps';
                C = strsplit(file_name, format);
                output_filename = strcat([strjoin(C(1)),fig_format]);
                hgexport(h, output_filename);
                pause(1);
                close(h);
            end
        end
    end
end
